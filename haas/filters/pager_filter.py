from haas.filters.filter import Filter

class PagerFilter(Filter):
    def __init__(self, tool, page_length=3200):
        super().__init__(tool)
        self.page_length = page_length
        self.cache = {}

    def paginate(self, result, current_page):
        # Break the result into pages, trying to break on whitespace
        pages = result.splitlines()

        # Accumulate lines into pages without exceeding the page_length
        paginated_result = []
        current_text = ""
        for line in pages:
            if len(current_text) + len(line) + 1 < self.page_length:
                current_text += (line + "\n")
            else:
                paginated_result.append(current_text)
                current_text = line + "\n"

        # Add any remaining text as a page
        if current_text:
            paginated_result.append(current_text)

        # Return the specified page and total page count
        page_output = paginated_result[current_page] if current_page < len(paginated_result) else ""
        return page_output, len(paginated_result)

    def do_it(self, *args, continue_paginate=False, **kwargs):
        cache_key = self.build_cache_key(args, kwargs)

        if not continue_paginate or cache_key not in self.cache:
            # Run the tool and cache the result with pagination.
            result = super().do_it(*args, **kwargs)
            page_output, total_pages = self.paginate(result, 0)
            self.cache[cache_key] = {"result": result, "page_count": total_pages, "current_page": 0}
        else:
            # Get the current page from the cache, then paginate
            cached_data = self.cache[cache_key]
            result = cached_data["result"]
            current_page = cached_data["current_page"]  # Keep track of the current page
            page_output, _ = self.paginate(result, current_page)
            cached_data["current_page"] += 1  # Increment the page for the next call

            if cached_data["current_page"] >= cached_data["page_count"]:
                del self.cache[cache_key]  # Remove from cache when all pages are read

        return {
            "content": page_output,
            "page_number": current_page + 1,
            "total_pages": cached_data["page_count"]
        }

    def build_cache_key(self, args, kwargs):
        # Construct a unique cache key based on the arguments
        return str(args) + str(kwargs)
