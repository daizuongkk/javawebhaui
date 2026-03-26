package com.daizuongkk.web.controller.web;

import com.daizuongkk.web.dto.response.ProductResponse;
import com.daizuongkk.web.service.ProductService;
import com.daizuongkk.web.util.PaginationUtils;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.util.List;

@WebServlet(name = "Shop", value = "/shop")
public class ShopController extends HttpServlet {

    private ProductService productService = new ProductService();


    public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        int size = PaginationUtils.parsePositiveInt(request.getParameter("size"), 9);
        int currentPage = PaginationUtils.parsePositiveInt(request.getParameter("page"), 1);

        long totalProducts = productService.countProducts();
        int totalPages = (int) Math.ceil(totalProducts / (double) size);
        if (totalPages < 1) {
            totalPages = 1;
        }

        if (currentPage > totalPages) {
            currentPage = totalPages;
        }

        List<ProductResponse> products = productService.getProductsByPage(currentPage, size);
        request.setAttribute("products", products);
        request.setAttribute("totalProducts", totalProducts);
        request.setAttribute("currentPage", currentPage);
        request.setAttribute("pageSize", size);
        request.setAttribute("totalPages", totalPages);
        request.getRequestDispatcher("views/pages/store.jsp").forward(request, response);


    }



}
