/**
 * Simple rate limiting middleware
 * Note: For production, consider using express-rate-limit package
 */

const rateLimitStore = new Map();

/**
 * Simple in-memory rate limiter
 * @param {Object} options - Rate limit options
 * @param {number} options.windowMs - Time window in milliseconds
 * @param {number} options.maxRequests - Maximum requests per window
 * @returns {Function} Express middleware
 */
function createRateLimiter(options = {}) {
  const windowMs = options.windowMs || 15 * 60 * 1000; // 15 minutes default
  const maxRequests = options.maxRequests || 100; // 100 requests per window default
  
  return (req, res, next) => {
    const clientId = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    
    // Get or create rate limit entry
    let entry = rateLimitStore.get(clientId);
    
    if (!entry || now - entry.resetTime > windowMs) {
      // Create new entry or reset expired entry
      entry = {
        count: 0,
        resetTime: now + windowMs
      };
      rateLimitStore.set(clientId, entry);
    }
    
    // Increment request count
    entry.count++;
    
    // Check if limit exceeded
    if (entry.count > maxRequests) {
      const retryAfter = Math.ceil((entry.resetTime - now) / 1000);
      res.setHeader('Retry-After', retryAfter);
      return res.status(429).json({
        error: 'Too many requests',
        message: `Rate limit exceeded. Please try again after ${retryAfter} seconds.`
      });
    }
    
    // Set rate limit headers
    res.setHeader('X-RateLimit-Limit', maxRequests);
    res.setHeader('X-RateLimit-Remaining', Math.max(0, maxRequests - entry.count));
    res.setHeader('X-RateLimit-Reset', new Date(entry.resetTime).toISOString());
    
    next();
  };
}

// Clean up old entries periodically
setInterval(() => {
  const now = Date.now();
  for (const [clientId, entry] of rateLimitStore.entries()) {
    if (now > entry.resetTime) {
      rateLimitStore.delete(clientId);
    }
  }
}, 60 * 1000); // Clean up every minute

module.exports = { createRateLimiter };

