function getApiEndpoint() {
    if (process.env.NODE_ENV === "prod") {
      // If API endpoint is specified in an environment variable with production deployment
      return process.env.PROF_API_ENDPOINT;
    } else {
      // Otherwise, use development endpoint
      return "http://localhost:5000";
    }
}

async function requestWrapper({
    path,
    method = "GET",
    data = null
  }) {
    let headers = {};
    if (data != null) {
      headers["Content-Type"] = "application/json";
    }
    
    const response = await fetch(
      `${getApiEndpoint()}${path}`, 
      {
        method,
        headers,
        body: data ? JSON.stringify(data) : null
      }
    );
  
    return {
      success: response.ok,
      data: await response.json()
    };
  }

const apiWrapper = {
    async testMethod() {
        return requestWrapper({
          path: '/',
          method: "GET"
        })
    },

    async insertRecord() {
        return requestWrapper({
            path: '/insert',
            method: 'POST',
            data: {}
        })
    },

    async updateRecord() {
        return requestWrapper({
            path: '/update',
            method: 'POST',
            data: {}
        })
    },

    async deleteRecord() {
        return requestWrapper({
            path: '/delete',
            method: 'POST',
            data: {}
        })
    },

    async searchRecords() {
        return requestWrapper({
            path: '/search',
            method: 'GET',
            data: {}
        })
    }
}

export default apiWrapper