import logo from "./logo.svg";
import "./App.css";
import { useState, useEffect } from "react";
import robo from "./assets/IMG_2740-ai-brush-removebg-dfi3huke.png";
// import ran from "./assets/random.webp";
const App = () => {
  const [csrfToken, setCsrfToken] = useState("");

  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const response = await fetch("/get_csrf_token/");
        const data = await response.json();
        setCsrfToken(data.csrfToken);
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
      }
    };

    fetchCsrfToken();
  }, []);

  const htmlFile = `
    <div class="card2" style="
    top:10px;
    bottom: 10px;
    left: 450px;">
      <h2 class="card-title">Upload .pkl File</h2>
      <p class="card-description"></p>
      <br />
      <form
        method="post"
        action="/handle_pkl_upload/"
        enctype="multipart/form-data"
      >
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}"
        sttle="background-color: #04AA6D;
        border: none;
        color: white;"/>
        <input
          type="file"
          name="pklFile"
          accept=".pkl"
          id="csv-dropzone"
          class="csv-button"
          style="margin-left: 100px; margin-top:10px;"
        />
        <div class="buttons-container" style="margin-left: 150px; margin-top: 10px;">
        <button type="submit" class="button-arounder">Upload PKL</button>
        </div>
      </form>
    </div>
  `;
  return (
    <div class="bodyy">
      <div class="header">
        <h1>Automata</h1>
      </div>
      <div class="area">
        <div class="home" id="home">
          <div class="home-content">
            <h3>Unlock the power of structured data</h3>
            <h1>AUTOMATA</h1>
            <p>
              With Automata at your disposal, you gain the ability to
              effortlessly introduce and showcase your groundbreaking machine
              learning advancements, fostering seamless interaction and
              utilization among individuals from all backgrounds and expertise
              levels.
            </p>
          </div>
          <div class="home-img">
            <img src={robo} alt="" />
          </div>
          <ul class="circles">
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
          </ul>
        </div>
      </div>
      <div dangerouslySetInnerHTML={{ __html: htmlFile }} />
      <div class="footer">
        <div class="waves">
          <div class="wave" id="wave1"></div>
          <div class="wave" id="wave2"></div>
          <div class="wave" id="wave3"></div>
          <div class="wave" id="wave4"></div>
        </div>
        <ul class="social-icon">
          <li class="social-icon__item">
            <a class="social-icon__link" href="#">
              <ion-icon name="logo-facebook"></ion-icon>
            </a>
          </li>
          <li class="social-icon__item">
            <a class="social-icon__link" href="#">
              <ion-icon name="logo-twitter"></ion-icon>
            </a>
          </li>
          <li class="social-icon__item">
            <a class="social-icon__link" href="#">
              <ion-icon name="logo-linkedin"></ion-icon>
            </a>
          </li>
          <li class="social-icon__item">
            <a class="social-icon__link" href="#">
              <ion-icon name="logo-instagram"></ion-icon>
            </a>
          </li>
        </ul>
        <ul class="menu">
          <li class="menu__item">
            <a class="menu__link" href="#">
              Home
            </a>
          </li>
          <li class="menu__item">
            <a class="menu__link" href="#">
              About
            </a>
          </li>
          <li class="menu__item">
            <a class="menu__link" href="#">
              Services
            </a>
          </li>
          <li class="menu__item">
            <a class="menu__link" href="#">
              Team
            </a>
          </li>
          <li class="menu__item">
            <a class="menu__link" href="#">
              Contact
            </a>
          </li>
        </ul>
        <p>&copy;2024 Team Reptiles of Roorkela | All Rights Reserved</p>
      </div>
    </div>
  );
};

export default App;
