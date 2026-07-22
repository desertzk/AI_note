#include <hip/hip_runtime.h>
#include <hip/hiprtc.h>

#include <cmath>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

#define HIP_CHECK(stmt)                                                           \
    do {                                                                          \
        hipError_t result = (stmt);                                               \
        if (result != hipSuccess) {                                               \
            std::cerr << "HIP error at " << __FILE__ << ":" << __LINE__         \
                      << ": " << hipGetErrorString(result) << std::endl;          \
            std::exit(EXIT_FAILURE);                                              \
        }                                                                         \
    } while (0)

#define HIPRTC_CHECK(stmt)                                                        \
    do {                                                                          \
        hiprtcResult result = (stmt);                                             \
        if (result != HIPRTC_SUCCESS) {                                           \
            std::cerr << "HIPRTC error at " << __FILE__ << ":" << __LINE__      \
                      << ": " << hiprtcGetErrorString(result) << std::endl;       \
            std::exit(EXIT_FAILURE);                                              \
        }                                                                         \
    } while (0)

const char* kernel_source = R"(
extern "C" __global__ void occupancy_kernel(float* output, int iterations) {
    unsigned int global_id = blockIdx.x * blockDim.x + threadIdx.x;
    float value = 1.0f + static_cast<float>(global_id & 31u) * 0.001f;

    for (int iteration = 0; iteration < iterations; ++iteration) {
        value = value * 1.00000011920928955078125f + 0.00000011920928955078125f;
    }

    output[global_id] = value;
}
)";

int main(int argc, char** argv) {
    const int block_size = 256;
    int iterations = (argc > 1) ? std::atoi(argv[1]) : 500000;
    if (iterations <= 0) {
        std::cerr << "iterations must be positive" << std::endl;
        return EXIT_FAILURE;
    }

    int device = 0;
    HIP_CHECK(hipGetDevice(&device));

    hipDeviceProp_t properties{};
    HIP_CHECK(hipGetDeviceProperties(&properties, device));

    std::string architecture = "--gpu-architecture=" + std::string(properties.gcnArchName);
    const char* options[] = {architecture.c_str()};

    hiprtcProgram program;
    HIPRTC_CHECK(hiprtcCreateProgram(
        &program, kernel_source, "occupancy_kernel.cu", 0, nullptr, nullptr));

    hiprtcResult compile_result = hiprtcCompileProgram(program, 1, options);
    if (compile_result != HIPRTC_SUCCESS) {
        size_t log_size = 0;
        HIPRTC_CHECK(hiprtcGetProgramLogSize(program, &log_size));
        std::vector<char> log(log_size);
        HIPRTC_CHECK(hiprtcGetProgramLog(program, log.data()));
        std::cerr << log.data() << std::endl;
        HIPRTC_CHECK(compile_result);
    }

    size_t code_size = 0;
    HIPRTC_CHECK(hiprtcGetCodeSize(program, &code_size));
    std::vector<char> code(code_size);
    HIPRTC_CHECK(hiprtcGetCode(program, code.data()));
    HIPRTC_CHECK(hiprtcDestroyProgram(&program));

    hipModule_t module;
    HIP_CHECK(hipModuleLoadData(&module, code.data()));

    hipFunction_t function;
    HIP_CHECK(hipModuleGetFunction(&function, module, "occupancy_kernel"));

    int active_blocks_per_cu = 0;
    HIP_CHECK(hipModuleOccupancyMaxActiveBlocksPerMultiprocessor(
        &active_blocks_per_cu, function, block_size, 0));

    if (active_blocks_per_cu <= 0) {
        std::cerr << "Occupancy API returned no active blocks" << std::endl;
        HIP_CHECK(hipModuleUnload(module));
        return EXIT_FAILURE;
    }

    const int cu_count = properties.multiProcessorCount;
    const int wave_size = properties.warpSize;
    const int waves_per_block = block_size / wave_size;
    const int resident_waves_per_cu = active_blocks_per_cu * waves_per_block;
    const int grid_blocks = cu_count * active_blocks_per_cu;
    const size_t thread_count = static_cast<size_t>(grid_blocks) * block_size;

    int maximum_waves_per_cu = 0;
    if (properties.maxThreadsPerMultiProcessor > 0) {
        maximum_waves_per_cu = properties.maxThreadsPerMultiProcessor / wave_size;
    }

    std::cout << "Device: " << properties.name << " (" << properties.gcnArchName << ")\n"
              << "CUs: " << cu_count << "\n"
              << "Wave size: " << wave_size << "\n"
              << "Block size: " << block_size << " threads\n"
              << "Active blocks per CU: " << active_blocks_per_cu << "\n"
              << "Resident waves per CU: " << resident_waves_per_cu << "\n"
              << "Maximum waves per CU: " << maximum_waves_per_cu << "\n"
              << "Grid: " << grid_blocks << " blocks, " << thread_count << " threads\n"
              << "Iterations: " << iterations << std::endl;

    float* output = nullptr;
    HIP_CHECK(hipMalloc(&output, thread_count * sizeof(float)));

    void* arguments[] = {&output, &iterations};

    hipEvent_t start;
    hipEvent_t stop;
    HIP_CHECK(hipEventCreate(&start));
    HIP_CHECK(hipEventCreate(&stop));

    HIP_CHECK(hipEventRecord(start, nullptr));
    HIP_CHECK(hipModuleLaunchKernel(
        function,
        static_cast<unsigned int>(grid_blocks), 1, 1,
        block_size, 1, 1,
        0,
        nullptr,
        arguments,
        nullptr));
    HIP_CHECK(hipEventRecord(stop, nullptr));
    HIP_CHECK(hipEventSynchronize(stop));

    float elapsed_ms = 0.0f;
    HIP_CHECK(hipEventElapsedTime(&elapsed_ms, start, stop));

    std::vector<float> host_output(thread_count);
    HIP_CHECK(hipMemcpy(host_output.data(), output, thread_count * sizeof(float),
                        hipMemcpyDeviceToHost));

    bool valid = true;
    for (size_t index = 0; index < host_output.size(); ++index) {
        if (!std::isfinite(host_output[index])) {
            std::cerr << "Non-finite result at index " << index << std::endl;
            valid = false;
            break;
        }
    }

    std::cout << "Kernel duration: " << elapsed_ms << " ms\n"
              << "First result: " << host_output.front() << "\n"
              << "Validation: " << (valid ? "passed" : "failed") << std::endl;

    HIP_CHECK(hipEventDestroy(start));
    HIP_CHECK(hipEventDestroy(stop));
    HIP_CHECK(hipFree(output));
    HIP_CHECK(hipModuleUnload(module));

    return valid ? EXIT_SUCCESS : EXIT_FAILURE;
}
