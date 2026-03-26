package com.daizuongkk.web.controller.web;

import com.daizuongkk.web.dto.response.ProductResponse;
import com.daizuongkk.web.service.ProductService;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.List;

@WebServlet(name = "Home", value = "/home")
public class HomeController extends HttpServlet {

	private ProductService productService;

	public void init() throws ServletException {
		productService = new ProductService();
	}

	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

		List<ProductResponse> products = productService.getLatestProducts(10);

		request.setAttribute("products", products);

		request.getRequestDispatcher("views/pages/home.jsp").forward(request, response);
	}

}
