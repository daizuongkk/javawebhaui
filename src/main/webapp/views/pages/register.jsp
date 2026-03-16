<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <title>Electro - Đăng Kí</title>
    <base href="${pageContext.request.contextPath}/">

    <!-- Google font -->
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,500,700" rel="stylesheet">

    <!-- Bootstrap -->
    <link type="text/css" rel="stylesheet" href="assets/css/bootstrap.min.css"/>

    <!-- Slick -->
    <link type="text/css" rel="stylesheet" href="assets/css/slick.css"/>
    <link type="text/css" rel="stylesheet" href="assets/css/slick-theme.css"/>

    <!-- nouislider -->
    <link type="text/css" rel="stylesheet" href="assets/css/nouislider.min.css"/>

    <!-- Font Awesome Icon -->
    <link rel="stylesheet" href="assets/css/font-awesome.min.css">

    <!-- Custom stlylesheet -->
    <link type="text/css" rel="stylesheet" href="assets/css/style.css"/>
    <link type="text/css" rel="stylesheet" href="assets/css/login.css"/>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>
<body>
<!-- HEADER -->

<header>


    <!-- MAIN HEADER -->
    <div id="header">
        <!-- container -->
        <div class="container">
            <!-- row -->
            <div class="row">
                <!-- LOGO -->
                <div class="col-md-3">
                    <div class="header-logo">
                        <a href="home" class="logo">
                            <img src="./assets/img/logo.png" alt="">
                        </a>
                    </div>
                </div>
                <!-- /LOGO -->

            </div>
            <!-- row -->
        </div>
        <!-- container -->
    </div>
    <!-- /MAIN HEADER -->
</header>
<!-- /HEADER -->


<%--Login Form--%>

<div class="section">
    <div class="container">
        <div class="row">

            <div class="col-md-12">
                <div class="row">
                    <div class="col-md-6">
                        <img class="login-banner center-block" src="./assets/img/red-login-banner.jpg" alt="login-banner">
                    </div>
                    <div class="col-md-6">
                        <div class="login-container center-block">
                            <div class="soft-card">
                                <div class="comfort-header">
                                    <div class="gentle-logo">
                                        <div class="logo-circle">
                                            <div class="comfort-icon">
                                                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                                    <path d="M16 2C8.3 2 2 8.3 2 16s6.3 14 14 14 14-6.3 14-14S23.7 2 16 2z"
                                                          fill="none"
                                                          stroke="currentColor" stroke-width="1.5"/>
                                                    <path d="M12 16a4 4 0 108 0" stroke="currentColor"
                                                          stroke-width="1.5"
                                                          stroke-linecap="round"/>
                                                    <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
                                                    <circle cx="20" cy="12" r="1.5" fill="currentColor"/>
                                                </svg>
                                            </div>
                                            <div class="gentle-glow"></div>
                                        </div>
                                    </div>
                                    <h1 class="comfort-title">Đăng kí tài khoản Electro!</h1>
                                    <p class="gentle-subtitle">Bắt đầu một trải nghiệm mua sắm không giới hạn!</p>
                                </div>

                                <c:if test="${not empty registerError}">
                                    <div class="alert alert-danger text-center" role="alert">${registerError}</div>
                                </c:if>

                                <form class="comfort-form" id="loginForm" novalidate action="register" method="post">
                                    <div class="soft-field">
                                        <div class="field-container">
                                            <input type="text" id="username" name="username" required
                                                   autocomplete="username" maxlength="32"
                                                   pattern="[A-Za-z][A-Za-z0-9._]{4,31}"
                                                   title="Bat dau bang chu cai, gom chu/so/._, do dai 5-32 ky tu"
                                                   value="${submittedUsername}">
                                            <label for="username">Tên đăng nhập</label>
                                            <div class="field-accent"></div>
                                        </div>
                                        <span class="gentle-error" id="usernameError"></span>
                                    </div>
                                    <div class="soft-field">
                                        <div class="field-container">
                                            <input type="email" id="email" name="email" required autocomplete="email" value="${submittedEmail}">

                                            <label for="email">Email</label>
                                            <div class="field-accent"></div>
                                        </div>
                                        <span class="gentle-error" id="emailError"></span>
                                    </div>
                                    <div class="soft-field">
                                        <div class="field-container">
                                            <input type="password" id="password" name="password" required
                                                   autocomplete="new-password" minlength="8" maxlength="64"
                                                   pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^A-Za-z0-9])\\S{8,64}"
                                                   title="8-64 ky tu, co chu hoa, chu thuong, so, ky tu dac biet, khong chua khoang trang">
                                            <label for="password">Mật khẩu</label>
                                            <div>
                                                <button type="button" class="gentle-toggle" id="passwordToggle"
                                                        aria-label="Toggle password visibility">
                                                    <div class="toggle-icon">
                                                        <svg class="eye-open" width="20" height="20" viewBox="0 0 20 20"
                                                             fill="none">
                                                            <path d="M10 3c-4.5 0-8.3 3.8-9 7 .7 3.2 4.5 7 9 7s8.3-3.8 9-7c-.7-3.2-4.5-7-9-7z"
                                                                  stroke="currentColor" stroke-width="1.5" fill="none"/>
                                                            <circle cx="10" cy="10" r="3" stroke="currentColor"
                                                                    stroke-width="1.5"
                                                                    fill="none"/>
                                                        </svg>
                                                        <svg class="eye-closed" width="20" height="20"
                                                             viewBox="0 0 20 20"
                                                             fill="none">
                                                            <path d="M3 3l14 14M8.5 8.5a3 3 0 004 4m2.5-2.5C15 10 12.5 7 10 7c-.5 0-1 .1-1.5.3M10 13c-2.5 0-4.5-2-5-3 .3-.6.7-1.2 1.2-1.7"
                                                                  stroke="currentColor" stroke-width="1.5"
                                                                  stroke-linecap="round"
                                                                  stroke-linejoin="round"/>
                                                        </svg>
                                                    </div>
                                                </button>

                                            </div>

                                            <div class="field-accent"></div>
                                        </div>
                                        <span class="gentle-error" id="passwordError"></span>
                                    </div>
                                    <div class="soft-field">
                                        <div class="field-container">
                                            <input type="password" id="passwordConfirm" name="passwordConfirm" required
                                                   autocomplete="new-password" minlength="8" maxlength="64">
                                            <label for="passwordConfirm">Xác nhận mật khẩu</label>
                                            <div>
                                                <button type="button" class="gentle-toggle" id="passwordToggle"
                                                        aria-label="Toggle password visibility">
                                                    <div class="toggle-icon">
                                                        <svg class="eye-open" width="20" height="20" viewBox="0 0 20 20"
                                                             fill="none">
                                                            <path d="M10 3c-4.5 0-8.3 3.8-9 7 .7 3.2 4.5 7 9 7s8.3-3.8 9-7c-.7-3.2-4.5-7-9-7z"
                                                                  stroke="currentColor" stroke-width="1.5" fill="none"/>
                                                            <circle cx="10" cy="10" r="3" stroke="currentColor"
                                                                    stroke-width="1.5"
                                                                    fill="none"/>
                                                        </svg>
                                                        <svg class="eye-closed" width="20" height="20"
                                                             viewBox="0 0 20 20"
                                                             fill="none">
                                                            <path d="M3 3l14 14M8.5 8.5a3 3 0 004 4m2.5-2.5C15 10 12.5 7 10 7c-.5 0-1 .1-1.5.3M10 13c-2.5 0-4.5-2-5-3 .3-.6.7-1.2 1.2-1.7"
                                                                  stroke="currentColor" stroke-width="1.5"
                                                                  stroke-linecap="round"
                                                                  stroke-linejoin="round"/>
                                                        </svg>
                                                    </div>
                                                </button>
                                            </div>

                                            <div class="field-accent"></div>
                                        </div>
                                        <span class="gentle-error" id="passwordConfirmError"></span>
                                    </div>
                                    <button type="submit" class="comfort-button">
                                        <div class="button-background"></div>
                                        <span class="button-text">ĐĂNG KÍ</span>
                                        <div class="button-loader">
                                            <div class="gentle-spinner">
                                                <div class="spinner-circle"></div>
                                            </div>
                                        </div>
                                        <div class="button-glow"></div>
                                    </button>
                                </form>
                                <div class="text-center">Bằng việc đăng kí, bạn đã đồng ý với Electro. về <span><a
                                        href="">Điều khoản dịch vụ</a></span> &amp; <span><a
                                        href="">Chính sách bảo mật.</a></span></div>
                                <div class="gentle-divider">
                                    <div class="divider-line"></div>
                                    <span class="divider-text">hoặc tiếp tục với</span>
                                    <div class="divider-line"></div>
                                </div>

                                <div class="comfort-social">
                                    <button type="button" class="social-soft">
                                        <div class="social-background"></div>
                                        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                                            <path d="M9 7.4v3.2h4.6c-.2 1-.8 1.8-1.6 2.4v2h2.6c1.5-1.4 2.4-3.4 2.4-5.8 0-.6 0-1.1-.1-1.6H9z"
                                                  fill="#4285F4"/>
                                            <path d="M9 17c2.2 0 4-0.7 5.4-1.9l-2.6-2c-.7.5-1.6.8-2.8.8-2.1 0-3.9-1.4-4.6-3.4H1.7v2.1C3.1 15.2 5.8 17 9 17z"
                                                  fill="#34A853"/>
                                            <path d="M4.4 10.5c-.2-.5-.2-1.1 0-1.6V6.8H1.7c-.6 1.2-.6 2.6 0 3.8l2.7-2.1z"
                                                  fill="#FBBC04"/>
                                            <path d="M9 4.2c1.2 0 2.3.4 3.1 1.2l2.3-2.3C12.9 1.8 11.1 1 9 1 5.8 1 3.1 2.8 1.7 5.4l2.7 2.1C5.1 5.6 6.9 4.2 9 4.2z"
                                                  fill="#EA4335"/>
                                        </svg>
                                        <span>Google</span>
                                        <div class="social-glow"></div>
                                    </button>

                                    <button type="button" class="social-soft">
                                        <div class="social-background"></div>
                                        <svg width="18" height="18" viewBox="0 0 18 18" fill="#1877F2">
                                            <path d="M18 9C18 4.03 13.97 0 9 0S0 4.03 0 9c0 4.49 3.29 8.21 7.59 9v-6.37H5.31V9h2.28V7.02c0-2.25 1.34-3.49 3.39-3.49.98 0 2.01.18 2.01.18v2.21h-1.13c-1.11 0-1.46.69-1.46 1.4V9h2.49l-.4 2.63H10.4V18C14.71 17.21 18 13.49 18 9z"/>
                                        </svg>
                                        <span>Facebook</span>
                                        <div class="social-glow"></div>
                                    </button>
                                </div>

                                <div class="comfort-signup">
                                    <span class="signup-text">Đã có tài khoản?</span>
                                    <a href="login" class="comfort-link signup-link">Đăng nhập</a>
                                </div>

                                <div class="gentle-success" id="successMessage">
                                    <div class="success-bloom">
                                        <div class="bloom-rings">
                                            <div class="bloom-ring ring-1"></div>
                                            <div class="bloom-ring ring-2"></div>
                                            <div class="bloom-ring ring-3"></div>
                                        </div>
                                        <div class="success-icon">
                                            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                                                <path d="M8 14l5 5 11-11" stroke="currentColor" stroke-width="2.5"
                                                      stroke-linecap="round"
                                                      stroke-linejoin="round"/>
                                            </svg>
                                        </div>
                                    </div>
                                    <h3 class="success-title">Chào mừng!</h3>
                                    <p class="success-desc">Đăng chuyển huướng tới trang chủ...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

        </div>

    </div>


</div>


<!-- SECTION -->
<div class="section">
    <!-- container -->
    <div class="container">
        <!-- row -->
        <div class="row">
        </div>
        <!-- /row -->
    </div>
    <!-- /container -->
</div>
<!-- /SECTION -->

<!-- NEWSLETTER -->
<div id="newsletter" class="section">
    <!-- container -->
    <div class="container">
        <!-- row -->
        <div class="row">
            <div class="col-md-12">
                <div class="newsletter">
                    <p>Sign Up for the <strong>NEWSLETTER</strong></p>
                    <form>
                        <%--                        <input class="input" type="email" placeholder="Enter Your Email">--%>
                        <input class="input" type="text" placeholder="Enter Your Email">
                        <button class="newsletter-btn"><i class="fa fa-envelope"></i> Subscribe</button>
                    </form>
                    <ul class="newsletter-follow">
                        <li>
                            <a href="fb.com/daizuongkk"><i class="fa fa-facebook"></i></a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-twitter"></i></a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-instagram"></i></a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-pinterest"></i></a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <!-- /row -->
    </div>
    <!-- /container -->
</div>
<!-- /NEWSLETTER -->

<!-- FOOTER -->
<%@ include file="../commons/footer.jsp" %>
<!-- /FOOTER -->

<!-- jQuery Plugins -->
<script src="assets/js/jquery.min.js"></script>
<script src="assets/js/bootstrap.min.js"></script>
<script src="assets/js/slick.min.js"></script>
<script src="assets/js/nouislider.min.js"></script>
<script src="assets/js/jquery.zoom.min.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/form-utils.js"></script>
<script src="assets/js/login.js"></script>

</body>
</html>
