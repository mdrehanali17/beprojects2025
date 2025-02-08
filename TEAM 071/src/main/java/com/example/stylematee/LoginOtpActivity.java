package com.example.stylematee;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.FirebaseException;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.PhoneAuthCredential;
import com.google.firebase.auth.PhoneAuthOptions;
import com.google.firebase.auth.PhoneAuthProvider;

import java.util.concurrent.TimeUnit;

public class LoginOtpActivity extends AppCompatActivity {

    private String phoneNumber;
    private String verificationId;
    private PhoneAuthProvider.ForceResendingToken resendToken;
    private FirebaseAuth mAuth;

    private EditText otpInput;
    private Button nextBtn;
    private ProgressBar progressBar;
    private TextView resendOtpText;

    private long timeoutSeconds = 60;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_otp);

        // Initialize Firebase Authentication instance
        mAuth = FirebaseAuth.getInstance();

        // Initialize UI components
        otpInput = findViewById(R.id.login_otp);
        nextBtn = findViewById(R.id.login_next_btn);
        progressBar = findViewById(R.id.login_progress_bar);
        resendOtpText = findViewById(R.id.resend_otp_textview);

        // Get phone number from the previous activity
        phoneNumber = getIntent().getStringExtra("phone");

        // Send OTP
        sendOtp(phoneNumber, false);

        // Handle "Next" button click
        nextBtn.setOnClickListener(v -> {
            String otp = otpInput.getText().toString().trim();
            if (otp.isEmpty() || otp.length() < 6) {
                otpInput.setError("Enter a valid OTP");
                otpInput.requestFocus();
                return;
            }
            verifyCode(otp);
        });

        // Handle "Resend OTP" text click
        resendOtpText.setOnClickListener(v -> sendOtp(phoneNumber, true));
    }

    // Send OTP to the provided phone number
    private void sendOtp(String phoneNumber, boolean isResend) {
        setInProgress(true);

        PhoneAuthOptions options = PhoneAuthOptions.newBuilder(mAuth)
                .setPhoneNumber(phoneNumber)       // Phone number to verify
                .setTimeout(timeoutSeconds, TimeUnit.SECONDS) // Timeout duration
                .setActivity(this)                // Activity (for callback binding)
                .setCallbacks(new PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
                    @Override
                    public void onVerificationCompleted(@NonNull PhoneAuthCredential credential) {
                        // Auto-retrieval or instant validation success
                        signInWithCredential(credential);
                    }

                    @Override
                    public void onVerificationFailed(@NonNull FirebaseException e) {
                        // Verification failed
                        runOnUiThread(() -> {
                            Toast.makeText(LoginOtpActivity.this, "Verification failed: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                        });
                        setInProgress(false);
                    }

                    @Override
                    public void onCodeSent(@NonNull String verificationId, @NonNull PhoneAuthProvider.ForceResendingToken token) {
                        // Code sent successfully
                        LoginOtpActivity.this.verificationId = verificationId;
                        resendToken = token;
                        runOnUiThread(() -> {
                            Toast.makeText(LoginOtpActivity.this, "OTP sent successfully.", Toast.LENGTH_SHORT).show();
                        });
                        setInProgress(false);
                    }
                }) // Callbacks
                .build();

        if (isResend && resendToken != null) {
            options = PhoneAuthOptions.newBuilder(mAuth)
                    .setPhoneNumber(phoneNumber)
                    .setTimeout(timeoutSeconds, TimeUnit.SECONDS)
                    .setActivity(this)
                    .setCallbacks(new PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
                        @Override
                        public void onVerificationCompleted(@NonNull PhoneAuthCredential credential) {
                            signInWithCredential(credential);
                        }

                        @Override
                        public void onVerificationFailed(@NonNull FirebaseException e) {
                            runOnUiThread(() -> {
                                Toast.makeText(LoginOtpActivity.this, "Verification failed: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                            });
                            setInProgress(false);
                        }

                        @Override
                        public void onCodeSent(@NonNull String verificationId, @NonNull PhoneAuthProvider.ForceResendingToken token) {
                            LoginOtpActivity.this.verificationId = verificationId;
                            resendToken = token;
                            runOnUiThread(() -> {
                                Toast.makeText(LoginOtpActivity.this, "OTP sent successfully.", Toast.LENGTH_SHORT).show();
                            });
                            setInProgress(false);
                        }
                    }) // Callbacks
                    .setForceResendingToken(resendToken) // Add resend token for resending
                    .build();
        }

        PhoneAuthProvider.verifyPhoneNumber(options);
    }

    // Set progress bar visibility
    private void setInProgress(boolean inProgress) {
        progressBar.setVisibility(inProgress ? View.VISIBLE : View.GONE);
        nextBtn.setVisibility(inProgress ? View.GONE : View.VISIBLE);
    }

    // Verify the entered OTP code
    private void verifyCode(String code) {
        PhoneAuthCredential credential = PhoneAuthProvider.getCredential(verificationId, code);
        signInWithCredential(credential);
    }

    // Sign in with the provided phone credential
    private void signInWithCredential(PhoneAuthCredential credential) {
        mAuth.signInWithCredential(credential).addOnCompleteListener(task -> {
            if (task.isSuccessful()) {
                Intent intent = new Intent(LoginOtpActivity.this, MainActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                startActivity(intent);
            } else {
                otpInput.setError("Invalid OTP");
                otpInput.requestFocus();
            }
        });
    }
}
