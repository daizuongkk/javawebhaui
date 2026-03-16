package com.daizuongkk.web.repository;

import com.daizuongkk.web.model.Role;
import com.daizuongkk.web.model.User;
import com.daizuongkk.web.util.JDBCUtils;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class UserRepository {
    private Connection connection;

    public UserRepository() {
        this.connection = JDBCUtils.getConnection();
    }

    // Shared connection is not thread-safe for parallel use, so serialize repository operations.
    public synchronized User findByUsernameOrEmail(String username) {
        if (username == null || username.trim().isEmpty()) {
            return null;
        }

        String sql = "SELECT * FROM users WHERE username = ? OR email = ?";
        try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
            statement.setString(1, username.trim());
            statement.setString(2, username.trim());
            ResultSet resultSet = statement.executeQuery();
            if (resultSet.next()) {
                User user = new User();
                user.setId(resultSet.getLong("id"));
                user.setUsername(resultSet.getString("username"));
                user.setPassword(resultSet.getString("password"));
                user.setRole(Role.valueOf(resultSet.getString("role")));
                user.setAvtUrl(resultSet.getString("avt_url"));
                user.setFirstName(resultSet.getString("first_name"));
                user.setLastName(resultSet.getString("last_name"));
                user.setPhone(resultSet.getString("phone"));
                user.setEmail(resultSet.getString("email"));
                user.setActive(resultSet.getBoolean("active"));
                user.setCreatedAt(resultSet.getTimestamp("created_at"));
                user.setUpdatedAt(resultSet.getTimestamp("updated_at"));
                return user;
            } else {
                return null;
            }
        } catch (Exception e) {

            e.printStackTrace();
            return null;
        }
    }

    public synchronized boolean existsByUsername(String username) {
        return exists("SELECT 1 FROM users WHERE username = ? LIMIT 1", username);
    }

    public synchronized boolean existsByEmail(String email) {
        return exists("SELECT 1 FROM users WHERE email = ? LIMIT 1", email);
    }

    public synchronized boolean create(User user) {
        String sql = "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)";
        try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
            statement.setString(1, user.getUsername());
            statement.setString(2, user.getEmail());
            statement.setString(3, user.getPassword());
            statement.setString(4, user.getRole().name());
            return statement.executeUpdate() > 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    private boolean exists(String sql, String value) {
        if (value == null || value.trim().isEmpty()) {
            return false;
        }

        try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
            statement.setString(1, value.trim());
            try (ResultSet resultSet = statement.executeQuery()) {
                return resultSet.next();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
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



}
