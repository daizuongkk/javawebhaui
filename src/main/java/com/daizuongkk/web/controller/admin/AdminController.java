package com.daizuongkk.web.controller.admin;


import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

@WebServlet(name = "AdminController", value = "/admin")
public class AdminController extends HttpServlet {

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
       String page =  request.getParameter("page");


       switch (page) {
           case "dashboard":
               response.sendRedirect("views/pages/admin-dashboard.jsp");
               return;
           case "users":
               response.sendRedirect("views/pages/users.jsp");
               return;
           case "inventory":
               response.sendRedirect("views/pages/inventory.jsp");
               return;
           case "reports":
               response.sendRedirect("views/pages/reports.jsp");
               return;
           case "add-product":
               response.sendRedirect("views/pages/create-product.jsp");
               return;
           default:
               response.sendRedirect("views/pages/admin-dashboard.jsp");
       }

    }


}
