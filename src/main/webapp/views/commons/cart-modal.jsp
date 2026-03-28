<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<div class="modal fade" id="cart-modal" tabindex="-1" role="dialog" aria-labelledby="cartModalTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="cartModalTitle">Giỏ hàng của bạn</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <div id="cart-modal-list">
                    <div class="empty-cart-message">Giỏ hàng đang trống</div>
                </div>
            </div>
            <div class="modal-footer" style="display:flex;justify-content:space-between;align-items:center;">
                <strong id="cart-modal-total">Tổng: $0.00</strong>
                <div>
                    <button type="button" class="btn btn-default" data-dismiss="modal">Đóng</button>
                    <a href="#" class="btn btn-primary">Thanh toán</a>
                </div>
            </div>
        </div>
    </div>
</div>

