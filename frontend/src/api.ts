export async function fetchSimilarUsers(page: number, minAge: number | null, maxAge: number | null): Promise<{ results: any[], total_pages: number }> {
  const params = new URLSearchParams();
  params.append('page', page.toString());
  if (minAge !== null) params.append('min_age', minAge.toString());
  if (maxAge !== null) params.append('max_age', maxAge.toString());

  const response = await fetch(`/api/similar-users/?${params.toString()}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
    },
  });
  return await response.json();
}