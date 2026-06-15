# Requirement: E-Commerce Order Processing

The system should provide a complete order processing workflow for the e-commerce platform.

Customers should be able to browse products, add items to cart, apply discount codes, and checkout.

The system should support multiple payment methods (credit card, PayPal, bank transfer, cash on delivery).

The system should calculate shipping costs based on weight, destination, and shipping method.

The system should manage inventory in real-time — when an order is placed, stock must be reserved and deducted.

The system should handle order status transitions: pending → paid → processing → shipped → delivered → completed.

The system should send email notifications to customers at each status change.

The system should support order cancellation and refunds with a clear approval workflow.

The system should enforce business rules: minimum order amount, maximum quantity per item, restricted shipping locations.

The order service should expose APIs for cart management, checkout, payment, shipping, and order tracking.
