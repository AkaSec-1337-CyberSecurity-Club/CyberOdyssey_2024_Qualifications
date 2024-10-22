<?php

error_reporting(0);
ini_set('display_errors', '0');

$backend_url = 'http://backend:8000/';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'register') {
    $username = $_POST['username'];
    $note = $_POST['note'];

    if (strlen($username) == 0) {
        die("Invalid username.");
    }

    if (strlen($note) > 120) {
        die("Note is too long.");
    }

    $data = array(
        "username" => $username,
        "isAdmin" => false,
        "note" => $note
    );

    $options = array(
        'http' => array(
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
        ),
    );

    $context  = stream_context_create($options);
    $result = file_get_contents($backend_url . '/register', false, $context);

    echo $result;
    die;
}

elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['action']) && $_GET['action'] === 'list') {
    $users_url = $backend_url . '/users';

    $users_json = file_get_contents($users_url);

    $users = json_decode($users_json, true);

    echo "<h2>User List</h2>";
    echo "<table border='1'>
            <tr>
                <th>Username</th>
                <th>Admin</th>
                <th>Note</th>
            </tr>";

    foreach ($users as $username => $details) {
        $safe_username = htmlspecialchars($username);
        $safe_note = htmlspecialchars($details['note']);
        $isAdmin = $details['isAdmin'] ? 'Yes' : 'No';

        echo "<tr>
                <td>{$safe_username}</td>
                <td>{$isAdmin}</td>
                <td>{$safe_note}</td>
            </tr>";
    }

    echo "</table>";
    die;
}

elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'beta') {
    $file_path = $_POST['file_path'];
    $note = $_POST['note'];

    file_put_contents($file_path, $note);
    die;
}

?>
<head>
    <title>Notes APP</title>
</head>

<h2>Register</h2>
<form method="POST">
    <input type="hidden" name="action" value="register">
    Username: <input type="text" name="username"><br>
    Note: <textarea name="note"></textarea><br>
    <input type="submit" value="Register">
</form>

<h2>List Users</h2>
<form method="GET">
    <input type="hidden" name="action" value="list">
    <input type="submit" value="List Users">
</form>

<h2>Customized User Store (WIP)</h2>
<form method="POST">
    <input type="hidden" name="action" value="beta">
    File Path: <input type="text" name="file_path"><br>
    Note: <textarea name="note"></textarea><br>
    <input type="submit" value="Submit">
</form>
