package com.daizuongkk.web.repository;

import com.daizuongkk.web.model.ProductImg;
import com.daizuongkk.web.util.JDBCUtils;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;

public class ProductImgRepository {
	private Connection connection;

	public ProductImgRepository() {
		this.connection = JDBCUtils.getConnection();
	}

	public ProductImgRepository(Connection connection) {
		this.connection = connection;
	}

	public synchronized List<ProductImg> findByProductId(Long productId) {
		if (productId == null || productId <= 0) {
			return Collections.emptyList();
		}

		String sql = "SELECT id, product_id, image_url FROM product_images WHERE product_id = ? ORDER BY id ASC";
		List<ProductImg> images = new ArrayList<>();

		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			try (ResultSet resultSet = statement.executeQuery()) {
				while (resultSet.next()) {
					images.add(resultSetToProductImg(resultSet));
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

		return images;
	}

	public synchronized List<String> findUrlsByProductId(Long productId) {
		if (productId == null || productId <= 0) {
			return Collections.emptyList();
		}

		String sql = "SELECT image_url FROM product_images WHERE product_id = ? ORDER BY id ASC";
		List<String> urls = new ArrayList<>();

		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			try (ResultSet resultSet = statement.executeQuery()) {
				while (resultSet.next()) {
					urls.add(resultSet.getString("image_url"));
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

		return urls;
	}

	public synchronized String findPrimaryUrlByProductId(Long productId) {
		if (productId == null || productId <= 0) {
			return null;
		}

		String sql = "SELECT image_url FROM product_images WHERE product_id = ? ORDER BY id ASC LIMIT 1";
		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			try (ResultSet resultSet = statement.executeQuery()) {
				if (resultSet.next()) {
					return resultSet.getString("image_url");
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}

	public synchronized boolean create(Long productId, String imageUrl) {
		if (productId == null || productId <= 0) {
			return false;
		}

		String normalizedUrl = normalizeUrl(imageUrl);
		if (normalizedUrl == null) {
			return false;
		}

		String sql = "INSERT INTO product_images (product_id, image_url) VALUES (?, ?)";
		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			statement.setString(2, normalizedUrl);
			return statement.executeUpdate() > 0;
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	public synchronized int createBatch(Long productId, List<String> imageUrls) {
		if (productId == null || productId <= 0 || imageUrls == null || imageUrls.isEmpty()) {
			return 0;
		}

		List<String> normalizedUrls = normalizeUniqueUrls(imageUrls);
		if (normalizedUrls.isEmpty()) {
			return 0;
		}

		String sql = "INSERT INTO product_images (product_id, image_url) VALUES (?, ?)";
		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			for (String normalizedUrl : normalizedUrls) {
				statement.setLong(1, productId);
				statement.setString(2, normalizedUrl);
				statement.addBatch();
			}

			int[] rows = statement.executeBatch();
			int affectedRows = 0;
			for (int row : rows) {
				if (row > 0) {
					affectedRows += row;
				}
			}
			return affectedRows;
		} catch (Exception e) {
			e.printStackTrace();
			return 0;
		}
	}

	public synchronized boolean deleteByProductId(Long productId) {
		if (productId == null || productId <= 0) {
			return false;
		}

		String sql = "DELETE FROM product_images WHERE product_id = ?";
		try (PreparedStatement statement = getConnection().prepareStatement(sql)) {
			statement.setLong(1, productId);
			statement.executeUpdate();
			return true;
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	public synchronized int replaceAllByProductId(Long productId, List<String> imageUrls) {
		if (productId == null || productId <= 0) {
			return 0;
		}

		List<String> normalizedUrls = normalizeUniqueUrls(imageUrls);

		Connection conn = getConnection();
		boolean autoCommit;
		try {
			autoCommit = conn.getAutoCommit();
			conn.setAutoCommit(false);

			try (PreparedStatement deleteStatement = conn.prepareStatement("DELETE FROM product_images WHERE product_id = ?")) {
				deleteStatement.setLong(1, productId);
				deleteStatement.executeUpdate();
			}

			int inserted = 0;
			if (!normalizedUrls.isEmpty()) {
				try (PreparedStatement insertStatement = conn.prepareStatement("INSERT INTO product_images (product_id, image_url) VALUES (?, ?)")) {
					for (String normalizedUrl : normalizedUrls) {
						insertStatement.setLong(1, productId);
						insertStatement.setString(2, normalizedUrl);
						insertStatement.addBatch();
					}

					int[] rows = insertStatement.executeBatch();
					for (int row : rows) {
						if (row > 0) {
							inserted += row;
						}
					}
				}
			}

			conn.commit();
			conn.setAutoCommit(autoCommit);
			return inserted;
		} catch (Exception e) {
			try {
				conn.rollback();
			} catch (SQLException rollbackException) {
				rollbackException.printStackTrace();
			}
			e.printStackTrace();
			return 0;
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

	private ProductImg resultSetToProductImg(ResultSet resultSet) throws SQLException {
		return ProductImg.builder()
				.id(resultSet.getLong("id"))
				.productId(resultSet.getLong("product_id"))
				.url(resultSet.getString("image_url"))
				.build();
	}

	private List<String> normalizeUniqueUrls(List<String> imageUrls) {
		if (imageUrls == null || imageUrls.isEmpty()) {
			return Collections.emptyList();
		}

		LinkedHashSet<String> uniqueUrls = new LinkedHashSet<>();
		for (String imageUrl : imageUrls) {
			String normalized = normalizeUrl(imageUrl);
			if (normalized != null) {
				uniqueUrls.add(normalized);
			}
		}
		return new ArrayList<>(uniqueUrls);
	}

	private String normalizeUrl(String imageUrl) {
		if (imageUrl == null) {
			return null;
		}

		String normalized = imageUrl.trim();
		return normalized.isEmpty() ? null : normalized;
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
}
