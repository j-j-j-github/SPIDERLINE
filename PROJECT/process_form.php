<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$to = "admin@spiderline.com";

require_once 'db_connect.php';

function sanitize_input($data)
{
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $form_type = isset($_POST['form_type']) ? sanitize_input($_POST['form_type']) : '';

    $subject = "";
    $message = "";
    $headers = "";

    if ($form_type === "service") {
        // Service Booking Form
        $name = isset($_POST['name']) ? sanitize_input($_POST['name']) : '';
        $email = isset($_POST['email']) ? sanitize_input($_POST['email']) : '';
        $mobile = isset($_POST['mobile']) ? sanitize_input($_POST['mobile']) : '';
        $date = isset($_POST['date']) ? sanitize_input($_POST['date']) : '';
        $vehicle_name = isset($_POST['vehicle_name']) ? sanitize_input($_POST['vehicle_name']) : '';
        $vehicle_number = isset($_POST['vehicle_number']) ? sanitize_input($_POST['vehicle_number']) : '';
        $location = isset($_POST['location']) ? sanitize_input($_POST['location']) : '';
        $description = isset($_POST['description']) ? sanitize_input($_POST['description']) : '';

        $subject = "New Service Booking Request from $name";

        $message = "You have received a new service booking request.\n\n";
        $message .= "Details:\n";
        $message .= "Name: $name\n";
        $message .= "Email: $email\n";
        $message .= "Mobile: $mobile\n";
        $message .= "Preferred Date: $date\n";
        $message .= "Vehicle Name: $vehicle_name\n";
        $message .= "Vehicle Number: $vehicle_number\n";
        $message .= "Dealer Location: $location\n";
        $message .= "Description: \n$description\n";

        $headers = "From: $email" . "\r\n" .
            "Reply-To: $email" . "\r\n" .
            "X-Mailer: PHP/" . phpversion();

        // Handle empty date for strict SQL mode
        if (empty($date))
            $date = null;

        // Insert into database
        try {
            $stmt = $pdo->prepare("INSERT INTO service_bookings (name, email, mobile, preferred_date, vehicle_name, vehicle_number, dealer_location, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
            $stmt->execute([$name, $email, $mobile, $date, $vehicle_name, $vehicle_number, $location, $description]);
        } catch (PDOException $e) {
            die("Database Error in Service Booking: " . $e->getMessage());
        }

    } elseif ($form_type === "vehicle_booking") {
        // Vehicle Booking Form
        $name = isset($_POST['name']) ? sanitize_input($_POST['name']) : '';
        $email = isset($_POST['email']) ? sanitize_input($_POST['email']) : '';
        $mobile = isset($_POST['mobile']) ? sanitize_input($_POST['mobile']) : '';
        $vehicle_name = isset($_POST['vehicle_name']) ? sanitize_input($_POST['vehicle_name']) : '';
        $location = isset($_POST['location']) ? sanitize_input($_POST['location']) : '';

        $subject = "New Vehicle Booking Request from $name";

        $message = "You have received a new vehicle booking request.\n\n";
        $message .= "Details:\n";
        $message .= "Name: $name\n";
        $message .= "Email: $email\n";
        $message .= "Mobile: $mobile\n";
        $message .= "Vehicle Name: $vehicle_name\n";
        $message .= "Preferred Dealer Location: $location\n";

        $headers = "From: $email" . "\r\n" .
            "Reply-To: $email" . "\r\n" .
            "X-Mailer: PHP/" . phpversion();

        // Insert into database
        try {
            $stmt = $pdo->prepare("INSERT INTO vehicle_bookings (name, email, mobile, vehicle_name, dealer_location) VALUES (?, ?, ?, ?, ?)");
            $stmt->execute([$name, $email, $mobile, $vehicle_name, $location]);
        } catch (PDOException $e) {
            die("Database Error in Vehicle Booking: " . $e->getMessage());
        }

    } elseif ($form_type === "contact") {
        // Contact Form
        $name = isset($_POST['name']) ? sanitize_input($_POST['name']) : '';
        $email = isset($_POST['email']) ? sanitize_input($_POST['email']) : '';
        $mobile = isset($_POST['mobile']) ? sanitize_input($_POST['mobile']) : '';
        $contact_type = isset($_POST['contact_type']) ? sanitize_input($_POST['contact_type']) : '';
        $user_message = isset($_POST['message']) ? sanitize_input($_POST['message']) : '';

        $subject = "New Enquiry: $contact_type from $name";

        $message = "You have received a new enquiry.\n\n";
        $message .= "Details:\n";
        $message .= "Name: $name\n";
        $message .= "Email: $email\n";
        $message .= "Mobile: $mobile\n";
        $message .= "Enquiry Type: $contact_type\n";
        $message .= "Message: \n$user_message\n";

        $headers = "From: $email" . "\r\n" .
            "Reply-To: $email" . "\r\n" .
            "X-Mailer: PHP/" . phpversion();

        // Insert into database
        try {
            $stmt = $pdo->prepare("INSERT INTO contact_enquiries (name, email, mobile, enquiry_type, message) VALUES (?, ?, ?, ?, ?)");
            $stmt->execute([$name, $email, $mobile, $contact_type, $user_message]);
        } catch (PDOException $e) {
            die("Database Error in Contact Form: " . $e->getMessage());
        }
    } else {
        header("Location: " . $_SERVER['HTTP_REFERER'] . "?status=error");
        exit;
    }

    // Send email
    if (mail($to, $subject, $message, $headers)) {
        $redirect_url = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'index.html';
        $parsed_url = parse_url($redirect_url);
        $base_url = $parsed_url['path'] ?? '';

        header("Location: " . $base_url . "?status=success");
        exit;
    } else {
        // email error
        $redirect_url = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'index.html';
        $parsed_url = parse_url($redirect_url);
        $base_url = $parsed_url['path'] ?? '';

        header("Location: " . $base_url . "?status=error");
        exit;
    }

} else {

    header("Location: index.html");
    exit;
}
?>