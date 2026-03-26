package com.daizuongkk.web.service;

import com.daizuongkk.web.dto.response.ReviewResponse;
import com.daizuongkk.web.repository.ReviewRepository;

import java.util.Collections;
import java.util.List;

public class ReviewService {
	private final ReviewRepository reviewRepository;

	public ReviewService() {
		this.reviewRepository = new ReviewRepository();
	}

	public ReviewService(ReviewRepository reviewRepository) {
		this.reviewRepository = reviewRepository;
	}

	public List<ReviewResponse> getReviewsByProductId(Long productId, int page, int size) {
		if (productId == null || productId <= 0) {
			return Collections.emptyList();
		}

		int normalizedPage = Math.max(page, 1);
		int normalizedSize = Math.max(size, 1);
		return reviewRepository.findByProductId(productId, normalizedPage, normalizedSize);
	}

	public boolean addReview(Long productId, Long userId, String feedback, int score) {
		if (productId == null || productId <= 0 || userId == null || userId <= 0) {
			return false;
		}

		if (score < 1 || score > 5) {
			return false;
		}

		if (reviewRepository.existsByProductIdAndUserId(productId, userId)) {
			return false;
		}

		return reviewRepository.create(productId, userId, feedback, score);
	}

	public long countReviewsByProductId(Long productId) {
		return reviewRepository.countByProductId(productId);
	}

	public double getAverageScoreByProductId(Long productId) {
		return reviewRepository.findAverageScoreByProductId(productId);
	}

	public boolean hasUserReviewedProduct(Long productId, Long userId) {
		return reviewRepository.existsByProductIdAndUserId(productId, userId);
	}
}
