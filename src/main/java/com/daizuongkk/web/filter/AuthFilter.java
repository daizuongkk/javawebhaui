package com.daizuongkk.web.filter;

import com.daizuongkk.web.dto.response.UserResponse;
import com.daizuongkk.web.model.Role;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebFilter;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;

@WebFilter("/*") // chặn toàn bộ request
public class AuthFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        String uri = req.getRequestURI();
        boolean isAdminArea = uri.contains("/admin")
                || uri.contains("/admin-dashboard.jsp")
                || uri.contains("/users.jsp")
                || uri.contains("/inventory.jsp")
                || uri.contains("/reports.jsp")
                || uri.contains("/create-product.jsp");


        // các trang KHÔNG cần login
        if (uri.contains("/login") ||
                uri.contains("/register") ||
                uri.contains("/assets") ||
                uri.contains("/home") ||
                uri.contains("/shop") ||
                uri.contains("/products")

        ) {

            chain.doFilter(request, response);
            return;
        }

        // check login
        HttpSession session = req.getSession(false);
        UserResponse account = session == null ? null : (UserResponse) session.getAttribute("account");
        if (isAdminArea) {
            if (account == null || account.getRole() != Role.ADMIN) {
                res.sendRedirect(req.getContextPath() + "/views/pages/error-page.jsp");
                return;
            }
        }
        if (account == null) {
            res.sendRedirect(req.getContextPath() + "/login");
        } else {
            chain.doFilter(request, response);
        }
    }
}