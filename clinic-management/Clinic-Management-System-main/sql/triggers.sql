-- ============================================================
-- CLINIC MANAGEMENT SYSTEM - ORACLE TRIGGERS
-- ============================================================

-- ============================================================
-- TRIGGER 1: Prevent double booking of appointments
-- The UNIQUE constraint already handles this at DB level,
-- but this trigger provides a clear error message.
-- ============================================================
CREATE OR REPLACE TRIGGER trg_prevent_double_booking
BEFORE INSERT ON APPOINTMENT
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO   v_count
    FROM   APPOINTMENT
    WHERE  doctor_id        = :NEW.doctor_id
      AND  appointment_date = :NEW.appointment_date
      AND  time_slot        = :NEW.time_slot
      AND  status           != 'Cancelled';  -- cancelled slots are re-bookable

    IF v_count > 0 THEN
        RAISE_APPLICATION_ERROR(
            -20001,
            'This time slot is already booked for the selected doctor on ' ||
            TO_CHAR(:NEW.appointment_date, 'DD-MON-YYYY') || ' at ' || :NEW.time_slot
        );
    END IF;
END;
/

-- ============================================================
-- TRIGGER 2: Auto-set billing payment_status to 'Paid'
-- when payment_mode is provided on INSERT
-- ============================================================
CREATE OR REPLACE TRIGGER trg_billing_auto_status
BEFORE INSERT ON BILLING
FOR EACH ROW
BEGIN
    IF :NEW.payment_mode IS NOT NULL AND :NEW.payment_status IS NULL THEN
        :NEW.payment_status := 'Paid';
    ELSIF :NEW.payment_status IS NULL THEN
        :NEW.payment_status := 'Pending';
    END IF;

    -- Auto-set billing date if not provided
    IF :NEW.billing_date IS NULL THEN
        :NEW.billing_date := SYSDATE;
    END IF;
END;
/

-- ============================================================
-- TRIGGER 3: Auto-update appointment status to 'Completed'
-- when a medical record is inserted for that appointment
-- ============================================================
CREATE OR REPLACE TRIGGER trg_appointment_complete
AFTER INSERT ON MEDICAL_RECORD
FOR EACH ROW
BEGIN
    UPDATE APPOINTMENT
    SET    status = 'Completed'
    WHERE  appointment_id = :NEW.appointment_id;
END;
/
