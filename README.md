<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Ouster Lidar Appnotes</h3>

</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
[![object_detection][object_detection]](https://example.com)
[![yolo_viz][yolo_viz]](https://example.com)
[![minecraft][minecraft]](https://example.com)
[![open3d][open3d]](https://example.com)


This project hosts a collection of high level application demo/code examples using Ouster's ![OSx Lidars](https://ouster.com/products/) and it's python ![ouster-sdk](https://static.ouster.dev/sdk-docs/quickstart.html).
We also provide hackable puzzle pieces to help inspire your prototyping efforts, ranging from AR/VR to Deep Learning applications. But we make sure that these snippets form a minimum viable application to give you the full context. Hobbyists/Students/Hackers welcome. Come make robots with OSx!

You'll find useful functional snippets to be reassembled like Lego pieces:
* Visualization (open3D/ouster-sdk)
* Practical large size point cloud pcap recording (event driven start/stop)
* Live sensor frame datafield processing
* Processing of Depth, Reflectivity information from lidar as an OpenCV 2D images
* Basic planar zone monitoring/triggering using OSx depth image + set computation 
* Plotting, and running basic 6DOF IMU sensor fusion from internal IMU
* Using SLAM map to create a digital game map asset
* Using pre-trained deep learning networks to perform object detection (Yolov5/PointPillars)
* Time/Frame synchronizing off the shelf camera to OSx lidars using strobe signal
* More to Come!  :smile:

google_colab_demos folder hosts examples that can be run on google colab without any hardware or software dependency.

hw_examples folder hosts examples that require an OSx sensor connected via gigE ethernet to the host computer.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [ouster-sdk](https://static.ouster.dev/sdk-docs/quickstart.html)
* [open3d](https://github.com/isl-org/Open3D)
* [shapely](https://github.com/shapely/shapely)
* [yolov5](https://github.com/ultralytics/yolov5)
* [google colab](https://colab.research.google.com/?utm_source=scs-index)
* [ahrs](https://github.com/Mayitzin/ahrs/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps, also available ![here](https://static.ouster.dev/sdk-docs/installation.html)

### Installation

* ouster-sdk
  ```sh
  python3 -m pip install --upgrade pip
  python3 -m pip install 'ouster-sdk[examples]'
  ```
  Verify installation
  ```sh
  python3 -m pip list
  ```
  You should see something like this:
  ```sh
  ouster-sdk                    0.3.0
  ```
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Othneil Drew's Best-README-Template](https://github.com/othneildrew/Best-README-Template)
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[object_detection]: https://storage.googleapis.com/data.ouster.io/concept-engineering/colab_images/yolo_result.png
[yolo_viz]: https://storage.googleapis.com/data.ouster.io/concept-engineering/colab_images/yolo_office_cropped.png
[minecraft]: https://storage.googleapis.com/data.ouster.io/concept-engineering/colab_images/minecraft_view1.png
[open3d]:https://storage.googleapis.com/data.ouster.io/concept-engineering/colab_images/newplot.png
