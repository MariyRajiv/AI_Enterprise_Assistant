import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const queryAssistant = async (sessionId, query) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/query`, {
      session_id: sessionId,
      query: query
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
