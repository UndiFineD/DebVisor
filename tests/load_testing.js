// DebVisor Load Testing Configuration
// k6 Load Testing Script
//
// Usage:
//   k6 run load_testing.js
//   k6 run --vus 100 --duration 5m load_testing.js
//   k6 run --out json=results.json load_testing.js
//
// Author: DebVisor Team
// Date: November 28, 2025

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Counter, Rate, Trend, Gauge } from 'k6/metrics';
import { randomIntBetween, randomItem, randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

// =============================================================================
// Configuration
// =============================================================================

export const options = {
    // Test scenarios
    scenarios: {
        // Smoke test - quick sanity check
        smoke: {
            executor: 'constant-vus',
            vus: 1,
            duration: '30s',
            gracefulStop: '5s',
            tags: { test_type: 'smoke' },
            env: { SCENARIO: 'smoke' },
        },

        // Load test - normal expected load
        load: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '2m', target: 50 },   // Ramp up to 50 users
                { duration: '5m', target: 50 },   // Stay at 50 users
                { duration: '2m', target: 100 },  // Ramp up to 100 users
                { duration: '5m', target: 100 },  // Stay at 100 users
                { duration: '2m', target: 0 },    // Ramp down
            ],
            gracefulStop: '30s',
            tags: { test_type: 'load' },
            env: { SCENARIO: 'load' },
            startTime: '35s',  // Start after smoke test
        },

        // Stress test - find breaking point
        stress: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '2m', target: 100 },
                { duration: '3m', target: 200 },
                { duration: '3m', target: 300 },
                { duration: '3m', target: 400 },
                { duration: '5m', target: 400 },  // Hold at peak
                { duration: '5m', target: 0 },    // Recovery
            ],
            gracefulStop: '60s',
            tags: { test_type: 'stress' },
            env: { SCENARIO: 'stress' },
            startTime: '20m',  // Start after load test
        },

        // Spike test - sudden traffic spike
        spike: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '1m', target: 50 },   // Normal load
                { duration: '10s', target: 500 }, // Spike!
                { duration: '3m', target: 500 },  // Hold spike
                { duration: '10s', target: 50 },  // Return to normal
                { duration: '3m', target: 50 },   // Continue normal
                { duration: '1m', target: 0 },
            ],
            gracefulStop: '30s',
            tags: { test_type: 'spike' },
            env: { SCENARIO: 'spike' },
            startTime: '45m',  // Start after stress test
        },

        // Soak test - extended duration
        soak: {
            executor: 'constant-vus',
            vus: 100,
            duration: '60m',
            gracefulStop: '60s',
            tags: { test_type: 'soak' },
            env: { SCENARIO: 'soak' },
            startTime: '55m',  // Start after spike test
        },
    },

    // Thresholds for pass/fail criteria
    thresholds: {
        // HTTP errors should be less than 1%
        http_req_failed: ['rate<0.01'],

        // 95% of requests should be below 500ms
        http_req_duration: ['p(95)<500', 'p(99)<1000'],

        // Custom metric thresholds
        'http_req_duration{endpoint:debts}': ['p(95)<300'],
        'http_req_duration{endpoint:payments}': ['p(95)<500'],
        'http_req_duration{endpoint:users}': ['p(95)<200'],

        // Error rates by endpoint
        'errors{endpoint:debts}': ['rate<0.01'],
        'errors{endpoint:payments}': ['rate<0.02'],

        // Throughput requirements
        'http_reqs{endpoint:debts}': ['rate>50'],
    },

    // Summary configuration
    summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
};

// =============================================================================
// Custom Metrics
// =============================================================================

const errors = new Counter('errors');
const successfulLogins = new Counter('successful_logins');
const failedLogins = new Counter('failed_logins');
const debtsCreated = new Counter('debts_created');
const paymentsProcessed = new Counter('payments_processed');

const loginDuration = new Trend('login_duration');
const debtCreationDuration = new Trend('debt_creation_duration');
const paymentDuration = new Trend('payment_duration');

const activeUsers = new Gauge('active_users');
const cacheHitRate = new Rate('cache_hit_rate');

// =============================================================================
// Test Data
// =============================================================================

const BASE_URL = __ENV.BASE_URL || 'http://localhost:5000';
const API_VERSION = __ENV.API_VERSION || 'v2';
const API_BASE = `${BASE_URL}/api/${API_VERSION}`;

// Test users
const TEST_USERS = [
    { email: 'test1@debvisor.com', password: 'TestPass123!' },
    { email: 'test2@debvisor.com', password: 'TestPass123!' },
    { email: 'test3@debvisor.com', password: 'TestPass123!' },
    { email: 'agent1@debvisor.com', password: 'AgentPass123!' },
    { email: 'admin@debvisor.com', password: 'AdminPass123!' },
];

// Debt types
const DEBT_TYPES = ['medical', 'credit_card', 'utility', 'student_loan', 'other'];

// Payment methods
const PAYMENT_METHODS = ['ach', 'card', 'check'];

// =============================================================================
// Helper Functions
// =============================================================================

function getAuthHeaders(token) {
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    };
}

function generateDebt() {
    return {
        debtor_id: `debtor-${randomString(8)}`,
        creditor_id: `creditor-${randomString(8)}`,
        original_amount: randomIntBetween(100, 50000),
        type: randomItem(DEBT_TYPES),
        due_date: new Date(Date.now() + randomIntBetween(30, 365) * 24 * 60 * 60 * 1000).toISOString(),
    };
}

function generatePayment(debtId) {
    return {
        debt_id: debtId,
        amount: randomIntBetween(10, 1000),
        method: randomItem(PAYMENT_METHODS),
    };
}

// =============================================================================
// Setup and Teardown
// =============================================================================

export function setup() {
    console.log(`Starting load test against ${BASE_URL}`);
    console.log(`Scenario: ${__ENV.SCENARIO || 'default'}`);

    // Verify service is available
    const healthCheck = http.get(`${BASE_URL}/health`);
    if (healthCheck.status !== 200) {
        throw new Error(`Service not healthy: ${healthCheck.status}`);
    }

    // Get authentication token for test user
    const loginRes = http.post(`${API_BASE}/auth/login`, JSON.stringify({
        email: TEST_USERS[0].email,
        password: TEST_USERS[0].password,
    }), {
        headers: { 'Content-Type': 'application/json' },
    });

    if (loginRes.status === 200) {
        const body = JSON.parse(loginRes.body);
        return { token: body.access_token };
    }

    console.warn('Could not obtain auth token, some tests may fail');
    return { token: null };
}

export function teardown(data) {
    console.log('Load test completed');
    console.log(`Total VUs used: ${__VU}`);
}

// =============================================================================
// Main Test Function
// =============================================================================

export default function(data) {
    const token = data.token;
    const headers = token ? getAuthHeaders(token) : { 'Content-Type': 'application/json' };

    // Update active users gauge
    activeUsers.add(__VU);

    // Run test groups
    group('Authentication', () => {
        testLogin();
    });

    group('Debt Operations', () => {
        testListDebts(headers);
        testGetDebt(headers);
        if (Math.random() < 0.3) {  // 30% of iterations create debts
            testCreateDebt(headers);
        }
    });

    group('Payment Operations', () => {
        testListPayments(headers);
        if (Math.random() < 0.2) {  // 20% of iterations create payments
            testCreatePayment(headers);
        }
    });

    group('User Operations', () => {
        testGetProfile(headers);
    });

    group('Search Operations', () => {
        testSearch(headers);
    });

    // Think time between iterations
    sleep(randomIntBetween(1, 3));
}

// =============================================================================
// Test Functions
// =============================================================================

function testLogin() {
    const user = randomItem(TEST_USERS);
    const startTime = Date.now();

    const res = http.post(`${API_BASE}/auth/login`, JSON.stringify({
        email: user.email,
        password: user.password,
    }), {
        headers: { 'Content-Type': 'application/json' },
        tags: { endpoint: 'login' },
    });

    const duration = Date.now() - startTime;
    loginDuration.add(duration);

    const success = check(res, {
        'login status is 200': (r) => r.status === 200,
        'login has token': (r) => JSON.parse(r.body).access_token !== undefined,
    });

    if (success) {
        successfulLogins.add(1);
    } else {
        failedLogins.add(1);
        errors.add(1, { endpoint: 'login' });
    }
}

function testListDebts(headers) {
    const page = randomIntBetween(1, 10);
    const perPage = randomIntBetween(10, 50);

    const res = http.get(`${API_BASE}/debts?page=${page}&per_page=${perPage}`, {
        headers: headers,
        tags: { endpoint: 'debts', operation: 'list' },
    });

    const success = check(res, {
        'list debts status is 200': (r) => r.status === 200,
        'list debts has data': (r) => JSON.parse(r.body).data !== undefined,
        'list debts has pagination': (r) => JSON.parse(r.body).pagination !== undefined,
    });

    if (!success) {
        errors.add(1, { endpoint: 'debts' });
    }

    // Check cache header for hit rate
    if (res.headers['X-Cache'] === 'HIT') {
        cacheHitRate.add(true);
    } else {
        cacheHitRate.add(false);
    }
}

function testGetDebt(headers) {
    // Use a known test debt ID or random
    const debtId = `debt-${randomString(8)}`;

    const res = http.get(`${API_BASE}/debts/${debtId}`, {
        headers: headers,
        tags: { endpoint: 'debts', operation: 'get' },
    });

    // 404 is acceptable for random IDs
    check(res, {
        'get debt status is 200 or 404': (r) => r.status === 200 || r.status === 404,
    });
}

function testCreateDebt(headers) {
    const debt = generateDebt();
    const startTime = Date.now();

    const res = http.post(`${API_BASE}/debts`, JSON.stringify(debt), {
        headers: headers,
        tags: { endpoint: 'debts', operation: 'create' },
    });

    const duration = Date.now() - startTime;
    debtCreationDuration.add(duration);

    const success = check(res, {
        'create debt status is 201': (r) => r.status === 201,
        'create debt has id': (r) => JSON.parse(r.body).id !== undefined,
    });

    if (success) {
        debtsCreated.add(1);
    } else {
        errors.add(1, { endpoint: 'debts' });
    }
}

function testListPayments(headers) {
    const res = http.get(`${API_BASE}/payments`, {
        headers: headers,
        tags: { endpoint: 'payments', operation: 'list' },
    });

    const success = check(res, {
        'list payments status is 200': (r) => r.status === 200,
    });

    if (!success) {
        errors.add(1, { endpoint: 'payments' });
    }
}

function testCreatePayment(headers) {
    const payment = generatePayment(`debt-${randomString(8)}`);
    const startTime = Date.now();

    const res = http.post(`${API_BASE}/payments`, JSON.stringify(payment), {
        headers: headers,
        tags: { endpoint: 'payments', operation: 'create' },
    });

    const duration = Date.now() - startTime;
    paymentDuration.add(duration);

    const success = check(res, {
        'create payment status is 201 or 400': (r) => r.status === 201 || r.status === 400,
    });

    if (res.status === 201) {
        paymentsProcessed.add(1);
    } else if (res.status >= 500) {
        errors.add(1, { endpoint: 'payments' });
    }
}

function testGetProfile(headers) {
    const res = http.get(`${API_BASE}/users/me`, {
        headers: headers,
        tags: { endpoint: 'users', operation: 'profile' },
    });

    check(res, {
        'get profile status is 200 or 401': (r) => r.status === 200 || r.status === 401,
    });
}

function testSearch(headers) {
    const searchTerms = ['medical', 'pending', 'overdue', 'paid'];
    const term = randomItem(searchTerms);

    const res = http.get(`${API_BASE}/search?q=${term}`, {
        headers: headers,
        tags: { endpoint: 'search' },
    });

    check(res, {
        'search status is 200': (r) => r.status === 200,
        'search response time < 1s': (r) => r.timings.duration < 1000,
    });
}

// =============================================================================
// Scenario-Specific Tests
// =============================================================================

export function smokeTest() {
    // Quick sanity check
    const res = http.get(`${BASE_URL}/health`);
    check(res, {
        'health check passes': (r) => r.status === 200,
    });
}

export function breakpointTest() {
    // Aggressive load to find breaking point
    const res = http.batch([
        ['GET', `${API_BASE}/debts`, null, { tags: { endpoint: 'debts' } }],
        ['GET', `${API_BASE}/payments`, null, { tags: { endpoint: 'payments' } }],
        ['GET', `${API_BASE}/users/me`, null, { tags: { endpoint: 'users' } }],
    ]);

    res.forEach((r, i) => {
        if (r.status >= 500) {
            errors.add(1);
        }
    });
}

// =============================================================================
// Custom Summary
// =============================================================================

export function handleSummary(data) {
    const summary = {
        timestamp: new Date().toISOString(),
        scenario: __ENV.SCENARIO || 'default',
        metrics: {
            http_reqs: data.metrics.http_reqs,
            http_req_duration: data.metrics.http_req_duration,
            http_req_failed: data.metrics.http_req_failed,
            errors: data.metrics.errors,
            successful_logins: data.metrics.successful_logins,
            debts_created: data.metrics.debts_created,
            payments_processed: data.metrics.payments_processed,
        },
        thresholds: data.thresholds,
    };

    return {
        'summary.json': JSON.stringify(summary, null, 2),
        'stdout': textSummary(data, { indent: '  ', enableColors: true }),
    };
}

function textSummary(data, opts) {
    // Simplified text summary
    let output = '\n';
    output += '='.repeat(60) + '\n';
    output += 'DEBVISOR LOAD TEST SUMMARY\n';
    output += '='.repeat(60) + '\n\n';

    output += `Scenario: ${__ENV.SCENARIO || 'default'}\n`;
    output += `Base URL: ${BASE_URL}\n\n`;

    if (data.metrics.http_reqs) {
        output += `Total Requests: ${data.metrics.http_reqs.values.count}\n`;
        output += `Requests/sec: ${data.metrics.http_reqs.values.rate.toFixed(2)}\n\n`;
    }

    if (data.metrics.http_req_duration) {
        output += `Response Times:\n`;
        output += `  Avg: ${data.metrics.http_req_duration.values.avg.toFixed(2)}ms\n`;
        output += `  P95: ${data.metrics.http_req_duration.values['p(95)'].toFixed(2)}ms\n`;
        output += `  P99: ${data.metrics.http_req_duration.values['p(99)'].toFixed(2)}ms\n\n`;
    }

    if (data.metrics.http_req_failed) {
        output += `Error Rate: ${(data.metrics.http_req_failed.values.rate * 100).toFixed(2)}%\n`;
    }

    output += '\n' + '='.repeat(60) + '\n';

    return output;
}
