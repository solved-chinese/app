import React from "react";
import ReactDom from "react-dom";
import "bootstrap/dist/css/bootstrap.css";


const Base = () => {
    return (
            <header class="full-width-bg-container" id="navbar-bg">
              <div class="card-container" id="navbar-container">
                <div class="main-content-container" id="navbar">
                  <a class="logo" href="{% url "index" %}"></a>
                  <div class="search-form-wrapper">
                    <div class="search-input-wrapper">
                      <i class="far fa-search search-icon"></i>
                      <input type="text" name="keyword" placeholder="Search Dictionary">
                    </div>
                    <div id="search-dropdown-wrapper">
                    </div>
                  </div>
                  {% if user.is_authenticated %}
                    <button class="button button-primary dropdown-toggle" id="userDropdown"
                            data-toggle="dropdown" aria-haspopup="true"
                            aria-expanded="false" href="{% url "profile" %}">
                      {{ user.get_display_name }}
                    </button>
                    <div class="dropdown-menu">
                      {% if user.is_staff %}
                        <a class="dropdown-item" href="{% url "staff_panel" %}">Staff Panel</a>
                        <a class="dropdown-item" href="{% url "admin:index" %}">Admin Panel</a>
                      {% endif %}
                      <a class="dropdown-item" href="{% url "profile" %}">Profile</a>
                      <a class="dropdown-item" href="{% url "logout" %}">Logout</a>
                    </div>
                  {% else %}
                    <a class="button button-text-only" href="{% url "login" %}">Login</a>
                    <a class="button button-primary" href="{% url "signup" %}">Sign Up</a>
                  {% endif %}
                </div>
              </div>
            </header>
                
            <div class="main-content-container" id="page-container">
              {% block content %}{% endblock content %}
            </div>
                
            <footer class="full-width-bg-container" id="footer-bg">
              <div class="main-content-container" id="footer">
                <span id="copyright-info">Solved Chinese &copy; 2019&ndash;2020.</span>
                <div id="footer-icon-container">
                  <a href="https://github.com/solved-chinese" class="footer-icon"><i class="fab fa-github"></i></a>
                  &nbsp;&nbsp;&nbsp;
                  <a href="{% url "about_us" %}" class="footer-icon">About</a>
                </div>
              </div>
            </footer>
    )
};