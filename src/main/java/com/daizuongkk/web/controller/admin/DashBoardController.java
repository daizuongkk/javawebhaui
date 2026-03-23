package com.daizuongkk.web.controller.admin;

import com.daizuongkk.web.dto.response.UserResponse;
import com.daizuongkk.web.model.Role;
import com.daizuongkk.web.model.User;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

@WebServlet(name = "AdminDashBoard", value = "/admin/dashboard")
public class DashBoardController extends HttpServlet {
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        if (request.getSession().getAttribute("account") == null) {
            response.sendRedirect(request.getContextPath() + "/login");
            return;
        }

        UserResponse user = (UserResponse) request.getSession().getAttribute("account");
        if (!user.getRole().equals(Role.ADMIN)) {
            response.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        response.sendRedirect(request.getContextPath() + "/views/pages/admin-dashboard.jsp");
    }

}
