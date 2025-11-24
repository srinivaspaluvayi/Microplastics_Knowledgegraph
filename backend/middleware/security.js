/**
 * Security middleware
 */

/**
 * Sets security headers
 */
function securityHeaders(req, res, next) {
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');
  
  // Prevent MIME type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');
  
  // Enable XSS protection
  res.setHeader('X-XSS-Protection', '1; mode=block');
  
  // Referrer policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // Content Security Policy
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; " +
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; " +
    "font-src 'self' https://cdn.jsdelivr.net; " +
    "img-src 'self' data:; " +
    "connect-src 'self';"
  );
  
  // Remove X-Powered-By header
  res.removeHeader('X-Powered-By');
  
  next();
}

/**
 * Error handler that prevents information disclosure
 */
function errorHandler(err, req, res, next) {
  // Log error for debugging (in production, use proper logging)
  console.error('Error:', err.message);
  
  // Don't expose error details to client
  res.status(err.status || 500).json({
    error: 'An error occurred',
    status: err.status || 500
  });
}

module.exports = {
  securityHeaders,
  errorHandler
};

