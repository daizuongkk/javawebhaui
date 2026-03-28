package com.daizuongkk.web.controller.web;

import com.daizuongkk.web.dto.request.SearchProductRequest;
import com.daizuongkk.web.dto.response.ProductResponse;
import com.daizuongkk.web.model.Brand;
import com.daizuongkk.web.model.Category;
import com.daizuongkk.web.service.ProductService;
import com.daizuongkk.web.util.PaginationUtils;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.List;

@WebServlet(name = "Shop", value = "/shop")
public class ShopController extends HttpServlet {

    private ProductService productService = new ProductService();


    public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        String name = request.getParameter("name");
        String sortBy = request.getParameter("sortBy");

        String[] categoryValues = request.getParameterValues("category");
        List<String> categories = (categoryValues != null && categoryValues.length > 0)
                ? List.of(categoryValues)
                : List.of();

        String[] brandValues = request.getParameterValues("brand");

        List<String> brands = (brandValues != null && brandValues.length > 0)
                ? List.of(brandValues)
                : List.of();

        Double minPrice = null;
        Double maxPrice = null;
        try {
            String minPriceParam = request.getParameter("minPrice");
            if (minPriceParam != null && !minPriceParam.trim().isEmpty()) {
                minPrice = Double.parseDouble(minPriceParam);
            }

            String maxPriceParam = request.getParameter("maxPrice");
            if (maxPriceParam != null && !maxPriceParam.trim().isEmpty()) {
                maxPrice = Double.parseDouble(maxPriceParam);
            }
        } catch (NumberFormatException e) {
        }

        SearchProductRequest filters = SearchProductRequest.builder()
                .name(name)
                .categories(categories)
                .brands(brands)
                .minPrice(minPrice)
                .maxPrice(maxPrice)
                .sortBy(sortBy)
                .build();

        int size = PaginationUtils.parsePositiveInt(request.getParameter("size"), 9);
        int currentPage = PaginationUtils.parsePositiveInt(request.getParameter("page"), 1);

        long totalProducts = productService.countProductsByFilter(filters);
        int totalPages = (int) Math.ceil(totalProducts / (double) size);
        if (totalPages < 1) {
            totalPages = 1;
        }

        if (currentPage > totalPages) {
            currentPage = totalPages;
        }
        List<ProductResponse> products = productService.getProductsByFilter(currentPage, size, filters);

        request.setAttribute("products", products);
        request.setAttribute("totalProducts", totalProducts);
        request.setAttribute("currentPage", currentPage);
        request.setAttribute("pageSize", size);
        request.setAttribute("totalPages", totalPages);
        request.setAttribute("categories", Category.getAlls());
        request.setAttribute("brands", Brand.getAlls());

        request.setAttribute("selectedCategories", categories);
        request.setAttribute("selectedBrands", brands);
        request.setAttribute("filterMinPrice", minPrice);
        request.setAttribute("filterMaxPrice", maxPrice);
        request.setAttribute("selectedSort", sortBy);
        request.setAttribute("filterName", name);

        request.getRequestDispatcher("views/pages/store.jsp").forward(request, response);
    }


}
