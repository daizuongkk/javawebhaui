package com.daizuongkk.web.controller.web;

import com.daizuongkk.web.dto.response.ProductResponse;
import com.daizuongkk.web.dto.response.ReviewResponse;
import com.daizuongkk.web.model.Category;
import com.daizuongkk.web.service.ProductService;
import com.daizuongkk.web.service.ReviewService;
import com.daizuongkk.web.util.PaginationUtils;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.List;

@WebServlet(name = "Products", value = "/products")
public class ProductController extends HttpServlet {
	private ProductService productService ;
	private ReviewService reviewService;

	@Override
	public void init() throws ServletException {
		productService = new ProductService();
		reviewService = new ReviewService();
	}

	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

		int currentPage = PaginationUtils.parsePositiveInt(request.getParameter("page"), 1);

		long totalProducts = productService.countProducts();
		int totalPages = (int) Math.ceil(totalProducts / (double) 3);
		if (totalPages < 1) {
			totalPages = 1;
		}

		if (currentPage > totalPages) {
			currentPage = totalPages;
		}

		Long productId = Long.parseLong(request.getParameter("id"));

		if (productId  == null) {
			response.sendError(HttpServletResponse.SC_BAD_REQUEST);
			return;
		}

		if (productId < 0) {
			response.sendRedirect(request.getContextPath() + "/home");
			return;
		}
		ProductResponse product = productService.getProductById(productId);

		if (product == null) {
			response.sendRedirect(request.getContextPath() + "/home");
			return;
		}

        request.setAttribute("categories", Category.getAlls());


        List<ReviewResponse>   reviews = reviewService.getReviewsByProductId(productId, currentPage,3);

		request.setAttribute("product", product);

		request.setAttribute("reviews", reviews);
		request.getRequestDispatcher("views/pages/product.jsp").forward(request, response);
	}


	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

	}


}
