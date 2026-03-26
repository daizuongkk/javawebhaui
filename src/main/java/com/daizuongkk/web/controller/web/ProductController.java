package com.daizuongkk.web.controller.web;

import com.daizuongkk.web.dto.response.ProductResponse;
import com.daizuongkk.web.model.Product;
import com.daizuongkk.web.service.ProductService;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.Collections;
import java.util.List;

@WebServlet(name = "Products", value = "/products")
public class ProductController extends HttpServlet {
	private ProductService productService = new ProductService();



	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

		String action = request.getParameter("action");


		int size = parsePositiveInt(request.getParameter("size"), 9);
		int currentPage = parsePositiveInt(request.getParameter("page"), 1);

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


	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String action = request.getParameter("action");
		if (action == null) {
			response.sendRedirect(request.getContextPath() + "/products");
			return;
		}

		response.sendRedirect(request.getContextPath() + "/products");
	}

	private int parsePositiveInt(String rawValue, int defaultValue) {
		if (rawValue == null || rawValue.trim().isEmpty()) {
			return defaultValue;
		}

		try {
			int parsed = Integer.parseInt(rawValue.trim());
			return parsed > 0 ? parsed : defaultValue;
		} catch (NumberFormatException ex) {
			return defaultValue;
		}
	}
}
