# TailorFlow Database Design Notes

## Overview

TailorFlow uses a hybrid database architecture.

- MySQL stores structured and relational data.
- MongoDB stores flexible order status history.
- Uploaded images are stored in the local uploads folder, while image metadata is stored in MySQL.

---

## Design Decisions

### Customer

- Phone number is unique.
- Customer information is stored in MySQL because it follows a fixed schema.

---

### Measurements

- Measurements are stored separately from orders.
- Measurement history is maintained.
- New measurement records are created only when measurements change.
- Measurements are garment-specific.

---

### Orders

- One customer can have multiple orders.
- One order can contain multiple products.

---

### Order Items

- Each order item references its own measurement.
- Unit price is stored for each item.
- Item status is maintained separately from overall order status.

---

### Payments

- Payments are transaction-based.
- One order can have multiple payment records.
- Remaining amount is calculated instead of stored.
- Transaction ID is optional because cash payments do not have one.

---

### Images

- Actual image files are stored in the uploads folder.
- Only image metadata is stored in MySQL.

---

## Future Enhancements

- WhatsApp reminders
- QR code receipts
- Revenue dashboard
- Fabric inventory
- Customer order history dashboard
- MongoDB-based order timeline