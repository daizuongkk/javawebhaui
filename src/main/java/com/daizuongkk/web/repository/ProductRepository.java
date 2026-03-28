package com.daizuongkk.web.repository;

import com.daizuongkk.web.dto.request.SearchProductRequest;
import com.daizuongkk.web.model.Product;
import com.daizuongkk.web.util.JDBCUtils;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


public class ProductRepository {
    private static final String SQL =
            "SELECT p.* FROM products p ";

    private Connection connection;

    public ProductRepository() {
        this.connection = JDBCUtils.getConnection();
    }

    public ProductRepository(Connection connection) {
        this.connection = connection;
    }

    public synchronized List<Product> findAll() {
        String sql = SQL + " ORDER BY p.created_at DESC";
        return findManyBySql(sql, statement -> {
        });
    }

    public synchronized List<Product> findPage(int page, int size) {
        int normalizedPage = Math.max(page, 1);
        int normalizedSize = Math.max(size, 1);
        int offset = (normalizedPage - 1) * normalizedSize;

        String sql = SQL + " ORDER BY RAND() LIMIT ? OFFSET ?";
        return findManyBySql(sql, statement -> {

            statement.setInt(1, normalizedSize);
            statement.setInt(2, offset);
        });
    }

    public List<Product> findByFilter(int page, int size, SearchProductRequest filters) {
        if (filters == null) {
            filters = SearchProductRequest.builder().build();
        }

        int normalizedPage = Math.max(page, 1);
        int normalizedSize = Math.max(size, 1);
        int offset = (normalizedPage - 1) * normalizedSize;

        StringBuilder sql = new StringBuilder(SQL + " WHERE 1=1");
        List<Object> params = buildFilterParams(sql, filters);

        // Add sorting
        sql.append(buildOrderClause(filters));
        sql.append(" LIMIT ? OFFSET ?");

        return findManyBySql(sql.toString(), statement -> {
            for (int i = 1; i <= params.size(); i++) {
                statement.setObject(i, params.get(i - 1));
            }

            statement.setInt(params.size() + 1, normalizedSize);
            statement.setInt(params.size() + 2, offset);
        });
    }

    public synchronized Product findById(Long id) {
        if (id == null) {
            return null;
        }

        String sql = SQL + " WHERE p.id = ? LIMIT 1";
        try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
            statement.setLong(1, id);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return resultSetToProduct(resultSet);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public synchronized List<Product> findByCategory(String category) {
        if (category == null || category.trim().isEmpty()) {
            return Collections.emptyList();
        }

        String sql = SQL + " WHERE p.category = ? ORDER BY p.created_at DESC";
        return findManyBySql(sql, statement -> statement.setString(1, category.trim()));
    }

    public synchronized List<Product> searchByName(String keyword) {
        if (keyword == null || keyword.trim().isEmpty()) {
            return Collections.emptyList();
        }

        String sql = SQL + " WHERE p.name LIKE ? ORDER BY p.created_at DESC";
        return findManyBySql(sql, statement -> statement.setString(1, "%" + keyword.trim() + "%"));
    }

    public synchronized List<Product> findLatest(int limit) {
        int normalizedLimit = Math.max(limit, 1);
        String sql = "SELECT * FROM ( SELECT * FROM products ORDER BY RAND() LIMIT ?) AS tmp ORDER BY created_at DESC";
        return findManyBySql(sql, statement -> statement.setInt(1, normalizedLimit));
    }

    public synchronized Long countAll() {
        String sql = "SELECT COUNT(*) FROM products";
        try (PreparedStatement statement = getConnection().prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            if (resultSet.next()) {
                return resultSet.getLong(1);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return 0L;
    }


    public Long countByCategory(String category) {
        if (category == null || category.trim().isEmpty()) {
            return 0L;
        }
        String sql = "SELECT COUNT(*) FROM products WHERE category = ?";
        try (PreparedStatement statement = getConnection().prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {

            // set params
            statement.setString(1, category.trim());

            if (resultSet.next()) {
                return resultSet.getLong(1);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return 0L;

    }

    public Long countByFilter(SearchProductRequest filters) {
        if (filters == null) {
            filters = SearchProductRequest.builder().build();
        }

        StringBuilder sql = new StringBuilder("SELECT COUNT(*) FROM products p WHERE 1=1 ");
        List<Object> params = buildFilterParams(sql, filters);

        // 1. Chỉ khởi tạo PreparedStatement trước
        try (PreparedStatement statement = getConnection().prepareStatement(sql.toString())) {

            // 2. PHẢI Set params TRƯỚC KHI execute
            for (int i = 0; i < params.size(); i++) {
                statement.setObject(i + 1, params.get(i));
            }

            // 3. Bây giờ mới thực thi và lấy ResultSet
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return resultSet.getLong(1);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        return 0L;
    }


    private String buildOrderClause(SearchProductRequest filters) {
        if (filters == null || filters.getSortBy() == null || filters.getSortBy().isBlank()) {
            return " ORDER BY p.created_at DESC";
        }

        return switch (filters.getSortBy().trim().toLowerCase()) {
            case "price_asc" -> " ORDER BY p.price ASC";
            case "price_desc" -> " ORDER BY p.price DESC";
            case "newest" -> " ORDER BY p.created_at DESC";
            case "oldest" -> " ORDER BY p.created_at ASC";
            default -> " ORDER BY p.created_at DESC";
        };
    }

    private List<Object> buildFilterParams(StringBuilder sql, SearchProductRequest filters) {
        List<Object> params = new ArrayList<>();

        if (filters == null) {
            return params;
        }

        List<String> categories = filters.getCategories();

        String name = filters.getName();

        if (name != null && !name.isBlank()) {
            sql.append(" AND p.name LIKE ?");
            params.add("%" + name.trim() + "%");
        }

        if (categories != null && !categories.isEmpty()) {
            sql.append(" AND p.category IN (").append(String.join(",", categories.stream().map(c -> "?").toList())).append(")");
            params.addAll(categories);
        }
        List<String> brands = filters.getBrands();

        if (brands != null && !brands.isEmpty()) {
            sql.append(" AND p.brand IN (").append(String.join(",", brands.stream().map(b -> "?").toList())).append(")");
            params.addAll(brands);
        }

        Double minPrice = filters.getMinPrice();
        if (minPrice != null) {
            sql.append(" AND p.price >= ?");
            params.add(minPrice);
        }

        Double maxPrice = filters.getMaxPrice();
        if (maxPrice != null) {
            sql.append(" AND p.price <= ?");
            params.add(maxPrice);
        }

        return params;
    }

    public synchronized void closeConnection() {
        if (this.connection == null) {
            return;
        }

        try {
            if (!this.connection.isClosed()) {
                this.connection.close();
            }
        } catch (SQLException e) {
            throw new RuntimeException("Cannot close database connection", e);
        }
    }

    private List<Product> findManyBySql(String sql, StatementBinder binder) {
        List<Product> products = new ArrayList<>();
        try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
            binder.bind(statement);
            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    products.add(resultSetToProduct(resultSet));
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return products;
    }

    private Product resultSetToProduct(ResultSet resultSet) throws SQLException {
        Double price = null;
        double rawPrice = resultSet.getDouble("price");
        if (!resultSet.wasNull()) {
            price = rawPrice;
        }

        return Product.builder()
                .id(resultSet.getLong("id"))
                .name(resultSet.getString("name"))
                .description(resultSet.getString("description"))
                .detail(resultSet.getString("detail"))
                .summary(resultSet.getString("summary"))
                .category(resultSet.getString("category"))
                .price(price)
                .promotion(resultSet.getLong("promotion"))
                .brand(resultSet.getString("brand"))
                .createdAt(resultSet.getTimestamp("created_at"))
                .updatedAt(resultSet.getTimestamp("updated_at"))
                .build();
    }

    private Connection getConnection() {
        try {
            if (this.connection == null || this.connection.isClosed()) {
                this.connection = JDBCUtils.getConnection();
            }
            return this.connection;
        } catch (SQLException e) {
            throw new RuntimeException("Cannot initialize database connection", e);
        }
    }


    @FunctionalInterface
    private interface StatementBinder {
        void bind(PreparedStatement statement) throws SQLException;
    }


}
