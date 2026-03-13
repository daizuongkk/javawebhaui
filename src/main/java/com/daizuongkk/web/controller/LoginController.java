package com.daizuongkk.web.controller;

import com.daizuongkk.web.dto.response.UserResponse;
import com.daizuongkk.web.service.AuthService;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

import java.io.IOException;
@NoArgsConstructor
@AllArgsConstructor
@WebServlet(name = "Login", value = "/login")
public class LoginController extends HttpServlet {

    private AuthService authService;

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.sendRedirect("views/pages/login.jsp");
    }


    @Override
    public void doPost(HttpServletRequest request,
                          HttpServletResponse response)
            throws IOException {

        String username = request.getParameter("username");
        String password = request.getParameter("password");


       UserResponse res =  authService.login(username, password);



        if (res == null) {
            response.sendRedirect("views/pages/login.jsp");
        }


        if (res.getRole().equals("ADMIN")) {
            response.sendRedirect("views/pages/admin.jsp");
        } else {
            response.sendRedirect("views/pages/home.jsp");
        }
    }
}
