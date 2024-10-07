fn xor_cipher(input: &str, key: &[u8]) -> Vec<u8> {
    input.bytes().enumerate().map(|(i, byte)| byte ^ key[i % key.len()]).collect()
}

// ODYSSEY{th3_fl4g_1s_r41s3d}
fn main() {
    let key: &[u8] = &[167, 49, 173, 150];
    let correct: Vec<u8> = vec![232, 117, 244, 197, 244, 116, 244, 237, 211, 89, 158, 201, 193, 93, 153, 241, 248, 0, 222, 201, 213, 5, 156, 229, 148, 85, 208];

    print!("whats the flag?: ");
    io::stdout().flush().unwrap();

    let mut user_input = String::new();
    io::stdin().read_line(&mut user_input).unwrap();
    let user_input = user_input.trim();
    let xored_input = xor_cipher(user_input, key);
    if xored_input == correct {
        println!("good job!");
    }
}