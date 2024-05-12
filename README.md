# gVulkan-artifact

This readme if for gVulkan(atc'24) artifact. gVulkan is the first multi-GPU acceleration rendering solution for Vulkan-based ray tracing.

The test environment for gVulkan must be a bare metal with multiple GPUs, or a docker/vm with passthough GPUs and GUI.

We have proved the feasibility of this solution under T4 * 4 (ali cloud), NVIDIA RTX3090 * 2, AMD 6800xt * 4. (ubuntu 20.04, ubuntu 22.04)

We have demonstrated the viability of the non-native solution under AMD 6800xt * 4 by simply changing the link port of the socket.

Our benckmark is a pure raytracing version of RayTracingInVulkan with the rasterization removed. https://github.com/funnygyc/RayTracingInVulkan-pureraytracing.git

First, we're going to run the original program directly in the environment. Since most original programs only use one GPU, there is no way to best utilize the performance of multiple GPUs. After launching our gVulkan and running the original program, the original program will utilize the arithmetic power of multiple GPUs to achieve higher FPS.

# Environment build

We have tested it on bare metal with NVIDIA RTX3090 * 2, ubuntu20.04. Other options (docker/vm with passthrough GPU and GUI) are theoretically feasible.

## Environment Installation

Install the basic dependency packages :

```
sudo apt install vim git ssh cmake build-essential openssh-server net-tools
```

Install the required dependencies for vcpkg :

```
sudo apt install curl libboost-all-dev libfreetype-dev libxinerama-dev libxcursor-dev libglfw3-dev libglm-dev xorg-dev libglu1-mesa-dev
```

Install the required dependencies for gVulkan :

```

sudo apt install ffmpeg libavcodec-dev libavformat-dev  libswscale-dev libsdl2-dev libsdl2-image-dev libxcb-image0-dev
```

Install the driver (if it is NVIDIA driver, you can refer to the following command) :

```
sudo apt install nvidia-driver-535
reboot
```

If nvidia-smi is able to obtain information about the GPU, the driver has been installed successfully

Install the Vulkan-SDK :

* [LunarXchange (lunarg.com)](https://vulkan.lunarg.com/)
* choose linux
* choose ubuntu package
* choose one version to download (more than 1.3)
* You can check your version by :

```
vulkaninfo | less
```

If cmake version is too old (less than 3.16), you should change the version of cmake :

* https://cmake.org/files -> download cmake-3.22.0-xxx-xxx.tar.gz ->tar -zxvf cmake-3.22.0-xxx-xxx.tar.gz
* vi ~/.bashrc
* put it on the last line : export PATH=$PATH:/home/username/filepath/cmake-3.12.2-Linux-x86_64/bin
* source ~/.bashrc

## Benchmark Installation

Download the [RayTracingInVulkan-pureraytracing](https://github.com/funnygyc/RayTracingInVulkan-pureraytracing) : 

```
git clone https://github.com/funnygyc/RayTracingInVulkan-pureraytracing.git
```

Go into RayTracingInVulkan-pureraytracing's folder :

```
cd RayTracingInVulkan-pureraytracing
```

Install vcpkg and benchmark :

```
./vcpkg_linux.sh

./build_linux.sh

cd build/linux/bin/
```

*RayTracer* is the benchmark. We can use --scene 1/2/3/4/5 to see other scenes.

When gVulkan needs to be enabled, you can use the following script, or manually enter the contents of the script.

```
../../../setEnvirOn.sh
```

## gVulkan( layer & server) Installation

gVulkan-artifact has two folder : vulkan_remote_layer_m_arm & vulkan_remote_server_benchmark.

vulkan_remote_layer_m_arm will compile the .so for the layer to use.

vulkan_remote_server_benchmark will compile the executable: demo_server, the server of gVulkan

### gVulkan layer Installation

Go into vulkan_remote_layer_m_arm's folder : 

```
cd vulkan_remote_layer_m_arm
```

you can use the following script, or manually enter the contents of the script.

compile the layer :

```
./compile_layer.sh
```

put the layer json in the folder it should be.

```
./put_json_to_folder.sh
```

### gVulkan server Installation

Go into vulkan_remote_server_benchmark's folder :

```
cd vulkan_remote_server_benchmark
```

you can use the following script, or manually enter the contents of the script.

compile the server :

```
./compile_server.sh

```

# Run the gVulkan

First, we need to run benchmark to make sure it's working properly :

```
cd RayTracingInVulkan-pureraytracing
cd build/linux/bin
./RayTracer > 1.txt
```

Next, we need to test that the layer is working properly.

```
../../../setEnvirOn.sh
```

If the benchmark doesn't work, it means that the layer is working.

At last, we run the gVulkan server.

```
cd vulkan_remote_server_benchmark
cd build
./DemoServer > 1.txt
```

At the same time, in another terminal, we run the benchmark with layer :

```
cd RayTracingInVulkan-pureraytracing
cd build/linux/bin
../../../setEnvirOn.sh
```

gVulkan is working. You can see the fps by the number on the window's title.
