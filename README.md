# Welcome!
<p align= "justify">
The purpose of this project is to analyze the growth and changes in the Internet Routing Domain since 1998. Using Autonomous System (AS) Relationship Graph datasets, we have gathered descriptive and quantitative metrics to compare each year. We have applied complex network analysis measurements to identify differences in Macro and Micro characteristics, such as Centrality, Network size, distance, robustness, and influence. The resulting data is presented on a visualisation dashboard, highlighting the disparities of change and the rate of evolution between two selected years. This platform is useful for identifying changes in ISP relationships, identifying providers, customers, and peer ASes, and determining the influence of individual domains over others. For more information, please refer to the images and installation instructions below.
</p>

# Images

<table>
  <tr>
    <td>
        <img src= "https://github.com/robdwhyte/InternetEvolution/blob/master/Images/Topological.PNG?raw=true">
    </td>
    <td>
        <img src= "https://github.com/robdwhyte/InternetEvolution/blob/master/Images/MacroCent.PNG?raw=true">
    </td>
  </tr>
  <tr>
    <td>
        <img src= "https://github.com/robdwhyte/InternetEvolution/blob/master/Images/MacroStat.PNG?raw=true">
    </td>
    <td>
        <img src= "https://github.com/robdwhyte/InternetEvolution/blob/master/Images/MicroStat.PNG?raw=true">
    </td>
  </tr>
  
</table>

# Installation instructions
### 1. Navigate to the assets folder and unzip the folders for topology renderings.

### 2. Set docker_build.sh & docker_run.sh as executable in linux terminal.

**chmod +x docker_build.sh && chmod +x docker_run.sh**

### 3. Run docker_build.sh and allow for the image to build.

**sudo ./docker_build.sh**

### 4. When finished building, run docker_run.sh.

**sudo ./docker_run.sh**

### 5. The container should be live. Visit localhost:8050 to use the interface :)
