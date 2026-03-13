package com.daizuongkk.web.util;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

@Getter
@Setter
@Builder
public class JDBCUtils {

	private final String url = "jdbc:mysql://localhost:3306/hauijavaweb";
	private final String user = "root";
	private final String password = "daizuongkk";

	public Connection getConnection() {
		try {
			return DriverManager.getConnection(url, user, password);
		} catch (SQLException e) {
			e.printStackTrace();
			return null;
		}
	}

}
