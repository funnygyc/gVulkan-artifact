# gVulkan-artifact

This readme if for gVulkan(ATC'24) artifact. gVulkan is the first multi-GPU acceleration rendering solution for Vulkan-based ray tracing.

The original pure raytracing application needed to be able to run in a current environment. However, the current application uses only one graphics card, which does not provide sufficient computing power. At the same time, only using the local graphics card increases the cost of graphics card replacement.

gVulkan will run transparently to the application. After launching our gVulkan and running the raw application, the raw application will utilize the computing power of multiple GPUs to achieve higher FPS while supporting GPUs in the cloud.

gVulkan is not dependent on a specific GPU and will work with any GPU that supports optical tracking (with RT core) and rendering (not compute cards). Our solution works on both AMD and NVIDIA ray-tracing GPUs.
gVulkan is not OS-specific. We implemented a toy version on Windows before. The current version requires some specific adaptations to run on Windows, but it is theoretically possible.
gVulkan is not dependent on a specific ISA. our solution has been shown to work on both arm and x86_64.

Our benchmark is a pure raytracing version of RayTracingInVulkan with the rasterization removed. https://github.com/funnygyc/RayTracingInVulkan-pureraytracing.git

# Hardware Requirements

The test environment for gVulkan must be a bare metal with **multiple GPUs**, or a docker/VM with **passthrough GPUs and GUI**.

All GPUs need to **support ray tracing (with RT core)** and **rendering (not compute cards)**, andpreferably of the same type.

If you want to test gVulkan on different machines, we expect the client to have the same type of GPU as the server, where the client has only one GPU and the server has multiple GPUs.

We have proved the feasibility of this solution under T4 * 4 (ali cloud), NVIDIA RTX3090 * 2, AMD 6800xt * 4. (ubuntu 20.04, ubuntu 22.04)

We have proved the feasibility of the non-native solution under AMD 6800xt * 4 by simply changing the link port of the socket. (Client has one AMD W6600/6800xt)

# Environment Build

We have tested it on bare metal with NVIDIA RTX3090 * 2, ubuntu20.04. Other options (docker/vm with passthrough GPU and GUI) are theoretically feasible.

## Environment Installation

### Install package

All the packages needed：

```
sudo apt install vim git ssh cmake build-essential openssh-server net-tools p7zip-full curl libboost-all-dev libfreetype-dev libxinerama-dev libxcursor-dev libglfw3-dev libglm-dev xorg-dev libglu1-mesa-dev ffmpeg libavcodec-dev libavformat-dev  libswscale-dev libsdl2-dev libsdl2-image-dev libxcb-image0-dev
```

#### More details :

Install the basic dependency packages :

```
sudo apt install vim git ssh cmake build-essential openssh-server net-tools p7zip-full
```

Install the required dependencies for vcpkg :

```
sudo apt install curl libboost-all-dev libfreetype-dev libxinerama-dev libxcursor-dev libglfw3-dev libglm-dev xorg-dev libglu1-mesa-dev
```

Install the required dependencies for gVulkan :

```

sudo apt install ffmpeg libavcodec-dev libavformat-dev  libswscale-dev libsdl2-dev libsdl2-image-dev libxcb-image0-dev
```

### Install the driver

If it is NVIDIA driver, you can refer to the following command :

```
sudo apt install nvidia-driver-535
reboot
```

If nvidia-smi is able to obtain information about the GPU, the driver has been installed successfully. (All nvidia drivers work)

### Install the Vulkan-SDK

download Vulkan-SDK in: [LunarXchange (lunarg.com)](https://vulkan.lunarg.com/).

choose linux download Vulkan-SDK in:

choose ubuntu package

choose one version to download (more than 1.3)()

Here's an example for ubuntu 20.04:

```
wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | sudo apt-key add -
sudo wget -qO /etc/apt/sources.list.d/lunarg-vulkan-1.3.280-focal.list https://packages.lunarg.com/vulkan/1.3.280/lunarg-vulkan-1.3.280-focal.list
sudo apt update
sudo apt install vulkan-sdk
```

You can check your version by :

```
vulkaninfo | less
```

### cmake version

If cmake version is too old (less than 3.16), you should change the version of cmake :

download Vulkan-SDK in: [Index of /files (cmake.org)](https://cmake.org/files/)

download cmake-3.22.0-xxx-xxx.tar.gz

tar -zxvf cmake-3.22.0-xxx-xxx.tar.gz

vi ~/.bashrc

put it on the last line : export PATH=$PATH:/home/username/filepath/cmake-3.22.0-xxx-xxx/bin (You need to modify this command according to the path of your generated *bin*)

source ~/.bashrc

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

*RayTracer* is the benchmark. We can use --scene 1/2/3/4/5 to see other scenes, such as

```
./RayTracer --scene 1 > 1.txt
```

When gVulkan needs to be enabled, you can use the following script, or manually enter the contents of the script.

```
../../../setEnvirOn.sh
```

## gVulkan( layer & server) Installation

You can get the gVulkan artifact at: https://github.com/funnygyc/gVulkan-artifact

```
git clone https://github.com/funnygyc/gVulkan-artifact.git
```

Unzip gVulkan-artifact-main.zip :

```
7z x gVulkan-artifact-main.zip -o./gVulkan-artifact-main
```

gVulkan-artifact-main has two folder : vulkan_remote_laye & vulkan_remote_server.

vulkan_remote_layer will compile the .so for the layer to use.

vulkan_remote_server will compile the executable: demo_server, the server of gVulkan

### gVulkan layer Installation

Go into vulkan_remote_layer's folder :

```
cd vulkan_remote_layer
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

Go into vulkan_remote_server's folder :

```
cd vulkan_remote_server
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
cd vulkan_remote_server
cd build
./DemoServer > 1.txt
```

At the same time, in another terminal, we run the benchmark with layer :

```
cd RayTracingInVulkan-pureraytracing
cd build/linux/bin
../../../setEnvirOn.sh
```

gVulkan is working. You can see the fps by the number on the window's title. You can also find out the time interval (in milliseconds) between each *CYCLE END 8* from the generated log file : `vulkan_remote_server/build/log`

# Others

## Other version of gVulkan

*gVulkan-artifact-multithreadDynamic* and *gVulkan-artifact-single* the other two gVulkan versions.

*gVulkan-artifact-multithreadDynamic* is a new version where the screen can be dynamic and the gpu computing power can be dynamic. You can use this version when testing dynamic effects, or in `gVulkan-artifact-main/vulkan_remote_server/include/multiGPUEnv.h` by adding `#define TESTDYNAMIC` (this version is for static screen.)

*gVulkan-artifact-single* is the baseline version of Fig.17.

## Change the GPU number used by gVulkan

If you want gVulkan use ` Num`  GPU, you can change `#define GPUNUM Num` in `gVulkan-artifact-main/vulkan_remote_server/include/multiGPUEnv.h`

## Layer and Server is not in the same Machine

If gVulkan's layer and server is not in the same machine, you can change the link IP of the layer to the IP address of the server :

change `127.0.0.1` to `Server IP` in `gVulkan-artifact-main/vulkan_remote_layer/include/clientSocket.h`.

# Test Configuration

## Simulating Dynamic Changes in GPU Computing Power

We lock the GPU to simulate a situation where the GPU is limited due to other applications.

sudo nvidia-smi -pm 1

sudo nvidia-smi -lgc 2000(according your GPU) -i 0 (card id, from 0 to n-1)

release :

sudo nvidia-smi -rgc

sudo nvidia-smi -pm 0

## Simulation of Network Latency

Locally, we simulate network latency via tc.

sudo tc qdisc add dev lo(dev name from ifconfig) root netem delay 1ms

reference: https://netbeez.net/blog/how-to-use-the-linux-traffic-control/
