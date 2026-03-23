<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ page isErrorPage="true" %>
<%
    Integer statusCode = (Integer) request.getAttribute("javax.servlet.error.status_code");
    String message = (String) request.getAttribute("javax.servlet.error.message");
%>
<!DOCTYPE html>
<html lang="en">

<head>
    <c:set var="pageTitle" value="404 Not Found"/></head>

<%@ include file="../commons/head.jsp" %>
<script type="module" crossorigin src="./assets/js/admin.js"></script>
<link rel="stylesheet" crossorigin href="./assets/css/admin.css">
</head>

<body style="background-color: black">

<div class="container d-flex align-items-center justify-content-center min-vh-100">
    <div class="" style="max-width: 500px; width: 100%;">
        <div class="text-center">
            <div class="mb-4">
                <a href="home" class="d-inline-block mb-4">
<%--                    <img src="data:image/svg+xml,%3csvg%20width='62'%20height='67'%20viewBox='0%200%2062%2067'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M30.604%2066.378L0.00805664%2048.1582V35.7825L30.604%2054.0023V66.378Z'%20fill='%23302C4D'/%3e%3cpath%20d='M61.1996%2048.1582L30.604%2066.378V54.0023L61.1996%2035.7825V48.1582Z'%20fill='%23E66239'/%3e%3cpath%20d='M30.5955%200L0%2018.2198V30.5955L30.5955%2012.3757V0Z'%20fill='%23657E92'/%3e%3cpath%20d='M61.191%2018.2198L30.5955%200V12.3757L61.191%2030.5955V18.2198Z'%20fill='%23A3B2BE'/%3e%3cpath%20d='M30.604%2048.8457L0.00805664%2030.6259V18.2498L30.604%2036.47V48.8457Z'%20fill='%23302C4D'/%3e%3cpath%20d='M61.1996%2030.6259L30.604%2048.8457V36.47L61.1996%2018.2498V30.6259Z'%20fill='%23E66239'/%3e%3c/svg%3e"--%>
<%--                         alt="" width="36">--%>
                    <span class="ms-2"><img src="./assets/img/logo.png" alt=""></span>
                </a>
            </div>

            <h1 class="display-1 fw-bold text-primary mb-2"><%= statusCode == null ? 404 : statusCode %></h1>
            <h2 class="card-title h4 mb-3"><%= message %></h2>
            <p class="text-muted mb-4">Bạn đã đi vào vùng cấm, hãy thoát ra bằng cách bấm nút bên dưới! </p>

            <a href="home" class="btn btn-primary">Chạy ngay đi</a>
        </div>
    </div>
</div>

<!-- Bootstrap JS -->

<%@ include file="../commons/script.jsp" %>

</body>

</html>
""