package com.daizuongkk.web.controller.web;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;

@WebServlet(name = "Shop", value = "/shop")
public class ShopController extends HttpServlet {
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {


        HttpSession session = request.getSession(false);

        boolean hasAccount = session != null && (session.getAttribute("account") != null || session.getAttribute("user") != null);
        if (!hasAccount) {
            response.sendRedirect("login");
            return;
        }
        request.getRequestDispatcher("views/pages/store.jsp").forward(request, response);
    }
}
