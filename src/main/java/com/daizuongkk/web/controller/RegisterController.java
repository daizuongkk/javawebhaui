package com.daizuongkk.web.controller;

import com.daizuongkk.web.service.AuthService;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

@WebServlet(name = "Register", value = "/register")
public class RegisterController extends HttpServlet {
    private AuthService authService;

    @Override
    public void init() {
        this.authService = new AuthService();
    }

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        request.getRequestDispatcher("/views/pages/register.jsp").forward(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        String username = trim(request.getParameter("username"));
        String email = trim(request.getParameter("email"));
        String password = request.getParameter("password");
        String passwordConfirm = request.getParameter("passwordConfirm");

        request.setAttribute("submittedUsername", username);
        request.setAttribute("submittedEmail", email);

        if (username.isEmpty() || email.isEmpty() || password == null || password.isEmpty()
                || passwordConfirm == null || passwordConfirm.isEmpty()) {
            request.setAttribute("registerError", "Vui lòng nhập đầy đủ thông tin đăng kí.");
            request.getRequestDispatcher("/views/pages/register.jsp").forward(request, response);
            return;
        }

        if (!password.equals(passwordConfirm)) {
            request.setAttribute("registerError", "Xác nhận mật khẩu không khớp.");
            request.getRequestDispatcher("/views/pages/register.jsp").forward(request, response);
            return;
        }

        AuthService.RegisterStatus status = authService.register(username, email, password);

        switch (status) {
            case INVALID_USERNAME_FORMAT -> request.setAttribute(
                    "registerError",
                    "Tên đăng nhập không hợp lệ. Bắt đầu bằng chữ cái, chỉ dùng chữ, số, dấu . hoặc _ (6-32 ký tự)."
            );
            case INVALID_EMAIL_FORMAT -> request.setAttribute("registerError", "Email không hơp lệ.");
            case INVALID_PASSWORD_FORMAT -> request.setAttribute(
                    "registerError",
                    "Mật khẩu phải 8–32 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt."
            );
            case USERNAME_EXISTS -> request.setAttribute("registerError", "Tên đăng nhập đã được sử dụng.");
            case EMAIL_EXISTS -> request.setAttribute("registerError", "Email đã được sử dụng.");
            case INVALID_INPUT -> request.setAttribute("registerError", "Dữ liệu không hợp lệ.");
            case FAILED -> request.setAttribute("registerError", "Đăng kí thất bại, vui lòng thử lại sau.");
            case SUCCESS -> {
                response.sendRedirect("login");
                return;
            }
        }

        request.getRequestDispatcher("/views/pages/register.jsp").forward(request, response);
    }

    private String trim(String value) {
        return value == null ? "" : value.trim();
    }

}
