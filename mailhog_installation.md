
# MailHog Installation Steps

1. Update package list and install Go programming language:
   ```bash
   sudo apt update
   sudo apt install golang-go
   ```

2. Verify Go installation:
   ```bash
   go version
   ```

3. Download the latest release of MailHog:
   ```bash
   wget https://github.com/mailhog/MailHog/releases/latest/download/MailHog_linux_amd64
   ```

4. Move the downloaded file to a directory in your PATH:
   ```bash
   sudo mv MailHog_linux_amd64 /usr/local/bin/mailhog
   ```

5. Make the MailHog binary executable:
   ```bash
   sudo chmod +x /usr/local/bin/mailhog
   ```

6. Start MailHog:
   ```bash
   mailhog
   ```

7. Access the MailHog web interface by navigating to:
   ```
   http://localhost:8025
   ```