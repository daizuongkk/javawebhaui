<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>

<c:url var="fallbackProductImage" value="/assets/img/product01.png"/>
<jsp:useBean id="now" class="java.util.Date" />
<style>
    .product {
        display: flex;
        flex-direction: column;
        height: 100%;
        min-height: 500px;
    }

    .product .product-img {
        width: 100%;
        height: 280px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f5f5f5;
        position: relative;
    }

    .product .product-img img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
    }

    .product .product-body {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        padding: 15px;
    }

    .product .product-name {
        margin: 5px 0;
        min-height: 50px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .product .product-price {
        margin: 5px 0;
        font-weight: bold;
    }

    .product .product-btns {
        margin-top: 10px;
    }

    .product .add-to-cart {
        padding: 10px;
        border-top: 1px solid #eee;
    }
</style>

<!-- product -->
<a href="${pageContext.request.contextPath}/products?id=${product.id}" class="product-link">
    <div class="product">
        <div class="product-img">
            <img src="${not empty product.imageUrl ? product.imageUrl[0] : fallbackProductImage}" alt="${product.name}">
            <div class="product-label">
                <c:if test="${product.promotion != null && product.promotion > 0}">
                    <span class="sale">-<c:out value="${product.promotion}"/>%</span>
                </c:if>
                <c:if test="${(now.time - product.createdAt.time) < (30 * 24 * 60 * 60 * 1000)}">
                    <span class="new">NEW</span>
                </c:if>
            </div>
        </div>
        <div class="product-body">
            <p class="product-category"><c:out value="${product.category}" default="N/A"/></p>
            <h3 class="product-name">
                <a href="${pageContext.request.contextPath}/products">
                    <c:out value="${product.name}"/>
                </a>
            </h3>
            <h4 class="product-price">
                <c:choose>
                    <c:when test="${product.price != null}">
                        $<fmt:formatNumber
                            value="${product.price - (product.price * product.promotion / 100)}"
                            type="number"
                            pattern="#.00" />
                    </c:when>
                    <c:otherwise>Contact</c:otherwise>
                </c:choose>
                <c:if test="${product.promotion != null && product.promotion > 0}">
                    <del class="product-old-price"><c:out value="${product.price}"/></del>
                </c:if>
            </h4>
            <div class="product-rating">
                <c:set target="${product}" property="reviewScore" value="${3}"/>
                <c:choose>
                    <c:when test="${product.reviewScore != 0}">
                        <c:forEach begin="1" end="${product.reviewScore}" var="i">
                            <i class="fa fa-star"></i>
                        </c:forEach>
                        <c:forEach begin="${product.reviewScore + 1}" end="5" var="i">
                            <i class="fa fa-star-o"></i>
                        </c:forEach>
                    </c:when>
                    <c:otherwise>
                        <c:forEach begin="1" end="5" var="i">
                            <i class="fa fa-star-o"></i>
                        </c:forEach>
                    </c:otherwise>
                </c:choose>


            </div>
            <div class="product-btns">
                <button class="add-to-wishlist"><i class="fa fa-heart-o"></i><span
                        class="tooltipp">thêm yêu thích</span>
                </button>
                <button class="add-to-compare"><i class="fa fa-exchange"></i><span
                        class="tooltipp">thêm so sánh</span>
                </button>
                <button class="quick-view"><i class="fa fa-eye"></i><span class="tooltipp">xem nhanh</span></button>
            </div>
        </div>
        <div class="add-to-cart">
            <button class="add-to-cart-btn"><i class="fa fa-shopping-cart"></i>Thêm Vào Giỏ</button>
        </div>
    </div>
</a>

