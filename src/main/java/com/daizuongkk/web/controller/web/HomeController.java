package com.daizuongkk.web.controller.web;

import com.daizuongkk.web.dto.response.ProductResponse;
import com.daizuongkk.web.model.Category;
import com.daizuongkk.web.service.ProductService;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@WebServlet(name = "Home", value = "/home")
public class HomeController extends HttpServlet {

	private ProductService productService;

	public void init() throws ServletException {
		productService = new ProductService();
	}

	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

		Map<String, String> categories = Category.getAlls();

		List<ProductResponse> products = productService.getLatestProducts(15);

		request.setAttribute("products", products);
		request.setAttribute("categories", categories);

		request.getRequestDispatcher("views/pages/home.jsp").forward(request, response);
	}

}
