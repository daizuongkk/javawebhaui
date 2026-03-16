package com.daizuongkk.web.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class JDBCUtils {

	private static final String DB_URL =
			"jdbc:mysql://localhost:3306/hauijavaweb?useSSL=false&serverTimezone=UTC";

	private static final String USER = "root";
	private static final String PASSWORD = "daizuongkk";

	static {
		try {
			Class.forName("com.mysql.cj.jdbc.Driver");
		} catch (ClassNotFoundException e) {
			throw new RuntimeException("MySQL Driver not found", e);
		}
	}

	public static Connection getConnection() {
		try {
			return DriverManager.getConnection(DB_URL, USER, PASSWORD);
		} catch (SQLException e) {
			throw new RuntimeException(e);
		}
	}
}