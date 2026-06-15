# Requirement: Order Approval Workflow

The system should provide an order approval workflow for sales orders exceeding a defined threshold.

When a sales order amount exceeds $10,000, it must go through a multi-level approval process.

Level 1: Sales Manager approval (orders $10,000 - $50,000).
Level 2: Regional Director approval (orders $50,000 - $100,000).
Level 3: VP of Sales approval (orders above $100,000).

The system should notify the approver via email and in-app notification when an order is pending their approval.

The system should record the approval history including approver, timestamp, and comments.

If an order is rejected, it should return to the sales representative with rejection reasons for revision.

The system should support delegation: if an approver is out of office, approvals can be delegated to a designated substitute.

The approval workflow should expose APIs for submitting orders for approval, approving, rejecting, and checking status.
