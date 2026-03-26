package com.daizuongkk.web.repository;

import com.daizuongkk.web.dto.response.ReviewResponse;
import com.daizuongkk.web.util.JDBCUtils;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ReviewRepository {
	private Connection connection;

	public ReviewRepository() {
		this.connection = JDBCUtils.getConnection();
	}

	public ReviewRepository(Connection connection) {
		this.connection = connection;
	}

	public synchronized List<ReviewResponse> findByProductId(Long productId, int page, int size) {
		if (productId == null || productId <= 0) {
			return Collections.emptyList();
		}

		int normalizedPage = Math.max(page, 1);
		int normalizedSize = Math.max(size, 1);
		int offset = (normalizedPage - 1) * normalizedSize;

		String sql = "SELECT r.id, r.product_id, r.user_id, r.feedback, r.score, r.created_at, " +
				"COALESCE(NULLIF(TRIM(CONCAT(u.first_name, ' ', u.last_name)), ''), u.username, 'Anonymous') AS user_display_name " +
				"FROM reviews r " +
				"LEFT JOIN users u ON u.id = r.user_id " +
				"WHERE r.product_id = ? " +
				"ORDER BY r.created_at DESC " +
				"LIMIT ? OFFSET ?";

		List<ReviewResponse> reviews = new ArrayList<>();
		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			statement.setInt(2, normalizedSize);
			statement.setInt(3, offset);

			try (ResultSet resultSet = statement.executeQuery()) {
				while (resultSet.next()) {
					reviews.add(resultSetToReview(resultSet));
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return reviews;
	}

	public synchronized boolean create(Long productId, Long userId, String feedback, int score) {
		if (productId == null || productId <= 0 || userId == null || userId <= 0) {
			return false;
		}

		String normalizedFeedback = feedback == null ? "" : feedback.trim();
		String sql = "INSERT INTO reviews (product_id, user_id, feedback, score) VALUES (?, ?, ?, ?)";

		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			statement.setLong(2, userId);
			statement.setString(3, normalizedFeedback);
			statement.setInt(4, score);
			return statement.executeUpdate() > 0;
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	public synchronized long countByProductId(Long productId) {
		if (productId == null || productId <= 0) {
			return 0;
		}

		String sql = "SELECT COUNT(*) FROM reviews WHERE product_id = ?";
		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			try (ResultSet resultSet = statement.executeQuery()) {
				if (resultSet.next()) {
					return resultSet.getLong(1);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return 0;
	}

	public synchronized Double findAverageScoreByProductId(Long productId) {
		if (productId == null || productId <= 0) {
			return 0.0;
		}

		String sql = "SELECT COALESCE(AVG(score), 0) FROM reviews WHERE product_id = ?";
		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			try (ResultSet resultSet = statement.executeQuery()) {
				if (resultSet.next()) {
					return resultSet.getDouble(1);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return 0.0;
	}

	public synchronized boolean existsByProductIdAndUserId(Long productId, Long userId) {
		if (productId == null || userId == null || productId <= 0 || userId <= 0) {
			return false;
		}

		String sql = "SELECT 1 FROM reviews WHERE product_id = ? AND user_id = ? LIMIT 1";
		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			statement.setLong(2, userId);
			try (ResultSet resultSet = statement.executeQuery()) {
				return resultSet.next();
			}
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	private ReviewResponse resultSetToReview(ResultSet resultSet) throws SQLException {
		return ReviewResponse.builder()
				.id(resultSet.getLong("id"))
				.productId(resultSet.getLong("product_id"))
				.userId(resultSet.getLong("user_id"))
				.userDisplayName(resultSet.getString("user_display_name"))
				.feedback(resultSet.getString("feedback"))
				.score(resultSet.getInt("score"))
				.createdAt(resultSet.getTimestamp("created_at"))
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
