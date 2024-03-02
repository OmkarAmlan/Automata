import logo from "./logo.svg";
import "./App.css";
import { useState, useEffect } from "react";
import robo from "./assets/IMG_2740-ai-brush-removebg-dfi3huke.png";
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
    left: 650px;">
      <img src="" alt="Card Image" class="card-image" />
      <h2 class="card-title">Card Title</h2>
      <p class="card-description">This is a sample card description.</p>
      <br />
      <form
        method="post"
        action="/handle_pkl_upload/"
        enctype="multipart/form-data"
      >
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}" />
        <input
          type="file"
          name="pklFile"
          accept=".pkl"
          id="csv-dropzone"
          class="csv-button"
        />
        <button type="submit">Upload PKL</button>
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
            <h3>Hello</h3>
            <h1>Automata</h1>
            <p>
              Automata revolutionizes your workflow by providing the tools to
              effortlessly construct and implement state-of-the-art machine
              learning models tailored for structured data. With this innovative
              platform, you can expedite the development process while ensuring
              scalability and efficiency. By leveraging Automata, you unlock the
              potential to rapidly iterate through model iterations, optimize
              performance, and seamlessly deploy solutions. Additionally, with
              its API endpoint, Automata enables seamless integration into your
              existing systems and workflows, further enhancing its utility and
              versatility. With Automata, you gain the ability to boost
              productivity and drive impactful outcomes across your
              organization.
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