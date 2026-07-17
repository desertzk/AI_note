#include <hip/hip_runtime.h>
#include <hip/hiprtc.h>  // Include HIPRTC headers
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cstdlib>

// Error checking macros
#define HIPRTC_CHECK(stmt)                                          \
    do {                                                            \
        hiprtcResult result = stmt;                                 \
        if (result != HIPRTC_SUCCESS) {                             \
            std::cerr << "HIPRTC error at " << __FILE__ << ":"      \
                      << __LINE__ << ": " << result << std::endl;   \
            std::cerr << "Error string: " << hiprtcGetErrorString(result) << std::endl; \
            exit(EXIT_FAILURE);                                     \
        }                                                           \
    } while (0)

#define HIP_CHECK(stmt)                                             \
    do {                                                            \
        hipError_t result = stmt;                                   \
        if (result != hipSuccess) {                                 \
            std::cerr << "HIP error at " << __FILE__ << ":"         \
                      << __LINE__ << ": " << hipGetErrorString(result) << std::endl; \
            exit(EXIT_FAILURE);                                     \
        }                                                           \
    } while (0)

// Kernel source code as a string
const char* kernel_code = R"(
extern "C" __global__ void vector_add(float* a, float* b, float* c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}
)";

int main() {
    std::cout << "HIPRTC Kernel Launch Demo with Code and Bitcode Dumping" << std::endl;
    hipError_t err;
    
    // 1. Create HIPRTC program
    hiprtcProgram prog;
    HIPRTC_CHECK(hiprtcCreateProgram(&prog, kernel_code, "vector_add.cu", 0, nullptr, nullptr));
    
    // 2. Get device properties to determine architecture
    int device;
    HIP_CHECK(hipGetDevice(&device));
    
    hipDeviceProp_t prop;
    HIP_CHECK(hipGetDeviceProperties(&prop, device));
    
    // 3. Compile the program with the target architecture flag.
    // NOTE: do NOT use -fgpu-rdc here. -fgpu-rdc produces LLVM bitcode only and
    // no loadable code object, so hiprtcGetCode()/hipModuleLoadData() would fail.
    std::string arch_flag = "--gpu-architecture=" + std::string(prop.gcnArchName);
    const char* opts[] = { arch_flag.c_str() };
    
    hiprtcResult compile_result = hiprtcCompileProgram(prog, 1, opts);
    
    // 4. Get compilation log if compilation fails
    if (compile_result != HIPRTC_SUCCESS) {
        size_t log_size;
        HIPRTC_CHECK(hiprtcGetProgramLogSize(prog, &log_size));
        std::vector<char> log(log_size);
        HIPRTC_CHECK(hiprtcGetProgramLog(prog, log.data()));
        std::cerr << "Compilation log:\n" << log.data() << std::endl;
        HIPRTC_CHECK(compile_result); // This will exit on failure
    }
    
    // 5. Get the compiled code (ISA) and Bitcode (IR)
    
    // A. Code Object (Execute & Dump Assembly)
    size_t code_size;
    HIPRTC_CHECK(hiprtcGetCodeSize(prog, &code_size));
    std::vector<char> code(code_size);
    HIPRTC_CHECK(hiprtcGetCode(prog, code.data()));
    std::cout << "Compiled code size: " << code_size << " bytes" << std::endl;
    
    std::ofstream codeFile("dump_kernel.co", std::ios::out | std::ios::binary);
    codeFile.write(code.data(), code_size);
    codeFile.close();
    
    std::cout << "Dumping assembly:" << std::endl;
    std::system("/opt/rocm/llvm/bin/llvm-objdump -d dump_kernel.co");

    // B. LLVM Bitcode (Dump IR) - requires a SEPARATE compile with -fgpu-rdc,
    // because the normal compile above yields a code object but no bitcode.
    hiprtcProgram prog_ir;
    HIPRTC_CHECK(hiprtcCreateProgram(&prog_ir, kernel_code, "vector_add.cu", 0, nullptr, nullptr));
    const char* opts_ir[] = { arch_flag.c_str(), "-fgpu-rdc" };
    HIPRTC_CHECK(hiprtcCompileProgram(prog_ir, 2, opts_ir));

    size_t bitcode_size;
    HIPRTC_CHECK(hiprtcGetBitcodeSize(prog_ir, &bitcode_size));
    std::vector<char> bitcode(bitcode_size);
    HIPRTC_CHECK(hiprtcGetBitcode(prog_ir, bitcode.data()));
    std::cout << "Bitcode size: " << bitcode_size << " bytes" << std::endl;

    std::ofstream bitcodeFile("dump_kernel.bc", std::ios::out | std::ios::binary);
    bitcodeFile.write(bitcode.data(), bitcode_size);
    bitcodeFile.close();

    std::cout << "Dumping LLVM IR:" << std::endl;
    std::system("/opt/rocm/llvm/bin/llvm-dis dump_kernel.bc"); 
    std::system("cat dump_kernel.ll");

    HIPRTC_CHECK(hiprtcDestroyProgram(&prog_ir));
    
    // 6. Destroy the HIPRTC program (no longer needed)
    HIPRTC_CHECK(hiprtcDestroyProgram(&prog));
    
    // 7. Load module from compiled binary data (the code object from -fgpu-rdc works for loading)
    hipModule_t module;
    err = hipModuleLoadData(&module, code.data());
    if (err != hipSuccess) {
        std::cerr << "Failed to load module: " << hipGetErrorString(err) << std::endl;
        return -1;
    }
    
    // 8. Get function from module
    hipFunction_t function;
    err = hipModuleGetFunction(&function, module, "vector_add");
    if (err != hipSuccess) {
        std::cerr << "Failed to get function: " << hipGetErrorString(err) << std::endl;
        (void)hipModuleUnload(module);
        return -1;
    }
    
    // 9. Prepare data
    const int N = 1024;
    float *d_a, *d_b, *d_c;
    float h_a[N], h_b[N], h_c[N];
    
    // Initialize host data
    for (int i = 0; i < N; i++) {
        h_a[i] = static_cast<float>(i);
        h_b[i] = static_cast<float>(i * 2);
    }
    
    // Allocate device memory
    HIP_CHECK(hipMalloc(&d_a, N * sizeof(float)));
    HIP_CHECK(hipMalloc(&d_b, N * sizeof(float)));
    HIP_CHECK(hipMalloc(&d_c, N * sizeof(float)));
    
    // Copy data to device
    HIP_CHECK(hipMemcpy(d_a, h_a, N * sizeof(float), hipMemcpyHostToDevice));
    HIP_CHECK(hipMemcpy(d_b, h_b, N * sizeof(float), hipMemcpyHostToDevice));
    
    // 10. Setup kernel arguments
    void* args[] = {&d_a, &d_b, &d_c, (void*)&N};
    
    // 11. Create stream
    hipStream_t stream;
    HIP_CHECK(hipStreamCreate(&stream));
    
    // 12. Launch kernel using hipModuleLaunchKernel
    uint32_t gridDimX = (N + 255) / 256;  // Calculate grid size
    uint32_t gridDimY = 1;
    uint32_t gridDimZ = 1;
    
    uint32_t blockDimX = 256;  // Block size
    uint32_t blockDimY = 1;
    uint32_t blockDimZ = 1;
    
    size_t sharedMemBytes = 0;  // No dynamic shared memory needed
    
    err = hipModuleLaunchKernel(
        function,           // Kernel function
        gridDimX, gridDimY, gridDimZ,  // Grid dimensions
        blockDimX, blockDimY, blockDimZ,  // Block dimensions
        sharedMemBytes,     // Shared memory size
        stream,             // Stream
        args,               // Kernel arguments
        nullptr             // Extra parameters
    );
    
    if (err != hipSuccess) {
        std::cerr << "Failed to launch kernel: " << hipGetErrorString(err) << std::endl;
    }
    
    // 13. Synchronize and copy results back
    HIP_CHECK(hipStreamSynchronize(stream));
    HIP_CHECK(hipMemcpy(h_c, d_c, N * sizeof(float), hipMemcpyDeviceToHost));
    
    // 14. Verify results
    bool success = true;
    for (int i = 0; i < N; i++) {
        float expected = h_a[i] + h_b[i];
        if (std::abs(h_c[i] - expected) > 1e-5f) {
            success = false;
            std::cout << "Verification failed at index " << i << ": "
                      << h_c[i] << " != " << expected << std::endl;
            break;
        }
    }
    
    if (success) {
        std::cout << "Vector addition completed successfully!" << std::endl;
        std::cout << "First 10 results: ";
        for (int i = 0; i < 10; i++) {
            std::cout << h_c[i] << " ";
        }
        std::cout << std::endl;
    }
    
    // 15. Cleanup
    HIP_CHECK(hipFree(d_a));
    HIP_CHECK(hipFree(d_b));
    HIP_CHECK(hipFree(d_c));
    HIP_CHECK(hipStreamDestroy(stream));
    HIP_CHECK(hipModuleUnload(module));
    
    return 0;
}
