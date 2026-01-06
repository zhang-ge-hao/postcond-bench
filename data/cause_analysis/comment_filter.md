[ ] AgentOps-AI--tokencost--count_string_tokens
https://github.com/AgentOps-AI/tokencost/blob/f5ca12cb0a979cc1d19a614615758ac04937fc6e/./tokencost/costs.py#L278-L305
```
def count_string_tokens(prompt: str, model: str) -> int:
    """
    Returns the number of tokens in a (prompt or completion) text string.

    Args:
        prompt (str): The text string
        model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
        int: The number of tokens in the text string.
    """
    model = model.lower()

    if "/" in model:
        model = model.split("/")[-1]

    if "claude-" in model:
        raise ValueError(
            "Warning: Anthropic does not support this method. Please use the `count_message_tokens` function for the exact counts."
        )

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(prompt))
```
[ ] Coreoz--Wisp--detectLongRunningJob
https://github.com/Coreoz/Wisp/blob/1076065124550231680c5ece56dbb281eeedcc1c/./src/main/java/com/coreoz/wisp/LongRunningJobMonitor.java#L75-L110
```
	/**
	 * Check whether a job is running for too long or not.
	 *
	 * @return true if the is running for too long, else false.
	 * Returned value is made available for testing purposes.
	 */
	boolean detectLongRunningJob(long currentTime, Job job) {
		if(job.status() == JobStatus.RUNNING && !longRunningJobs.containsKey(job)) {
			int jobExecutionsCount = job.executionsCount();
			Long jobStartedtimeInMillis = job.lastExecutionStartedTimeInMillis();
			Thread threadRunningJob = job.threadRunningJob();

			if(jobStartedtimeInMillis != null
				&& threadRunningJob != null
				&& currentTime - jobStartedtimeInMillis > detectionThresholdInMillis) {
				logger.warn(
					"Job '{}' is still running after {}ms (detection threshold = {}ms), stack trace = {}",
					job.name(),
					currentTime - jobStartedtimeInMillis,
					detectionThresholdInMillis,
					Stream
						.of(threadRunningJob.getStackTrace())
						.map(StackTraceElement::toString)
						.collect(Collectors.joining("\n  "))
				);

				longRunningJobs.put(
					job,
					new LongRunningJobInfo(jobStartedtimeInMillis, jobExecutionsCount)
				);

				return true;
			}
		}
		return false;
	}
```
[ ] D4Vinci--Scrapling--find_similar
https://github.com/D4Vinci/Scrapling/blob/d02da49865049d5175325943f1308f0c8b6101d2/./scrapling/parser.py#L1050-L1106
```
    def find_similar(
        self,
        similarity_threshold: float = 0.2,
        ignore_attributes: List | Tuple = (
            "href",
            "src",
        ),
        match_text: bool = False,
    ) -> "Selectors":
        """Find elements that are in the same tree depth in the page with the same tag name and same parent tag etc...
        then return the ones that match the current element attributes with a percentage higher than the input threshold.

        This function is inspired by AutoScraper and made for cases where you, for example, found a product div inside
        a products-list container and want to find other products using that element as a starting point EXCEPT
        this function works in any case without depending on the element type.

        :param similarity_threshold: The percentage to use while comparing element attributes.
            Note: Elements found before attributes matching/comparison will be sharing the same depth, same tag name,
            same parent tag name, and same grand parent tag name. So they are 99% likely to be correct unless you are
            extremely unlucky, then attributes matching comes into play, so don't play with this number unless
            you are getting the results you don't want.
            Also, if the current element doesn't have attributes and the similar element as well, then it's a 100% match.
        :param ignore_attributes: Attribute names passed will be ignored while matching the attributes in the last step.
            The default value is to ignore `href` and `src` as URLs can change a lot between elements, so it's unreliable
        :param match_text: If True, element text content will be taken into calculation while matching.
            Not recommended to use in normal cases, but it depends.

        :return: A ``Selectors`` container of ``Selector`` objects or empty list
        """
        # We will use the elements' root from now on to get the speed boost of using Lxml directly
        root = self._root
        similar_elements = list()

        current_depth = len(list(root.iterancestors()))
        target_attrs = self.__get_attributes(root, ignore_attributes) if ignore_attributes else root.attrib

        path_parts = [self.tag]
        if (parent := root.getparent()) is not None:
            path_parts.insert(0, parent.tag)
            if (grandparent := parent.getparent()) is not None:
                path_parts.insert(0, grandparent.tag)

        xpath_path = "//{}".format("/".join(path_parts))
        potential_matches = root.xpath(f"{xpath_path}[count(ancestor::*) = {current_depth}]")

        for potential_match in potential_matches:
            if potential_match != root and self.__are_alike(
                root,
                target_attrs,
                potential_match,
                ignore_attributes,
                similarity_threshold,
                match_text,
            ):
                similar_elements.append(potential_match)

        return Selectors(map(self.__element_convertor, similar_elements))
```
[ ] FasterXML--java-classmate--resolveMemberFields
https://github.com/FasterXML/java-classmate/blob/f9841eaf0a30f8b29c0b405c16219585480a58a6/./src/main/java/com/fasterxml/classmate/ResolvedTypeWithMembers.java#L264-L309
```
    /**
     * Method for fully resolving field definitions and associated annotations.
     * Neither field definitions nor associated annotations inherit, but we may
     * still need to add annotation overrides, as well as filter out filters
     * and annotations that caller is not interested in.
     */
    protected ResolvedField[] resolveMemberFields()
    {
        LinkedHashMap<String, ResolvedField> fields = new LinkedHashMap<String, ResolvedField>();

        /* Fields need different handling: must start from bottom; and annotations only get added
         * as overrides, never as defaults. And sub-classes fully mask fields. This makes
         * handling bit simpler than that of member methods.
         */
        for (int typeIndex = _types.length; --typeIndex >= 0; ) {
            HierarchicType thisType = _types[typeIndex];
            // If it's just a mix-in, add annotations as overrides
            if (thisType.isMixin()) {
                for (RawField raw : thisType.getType().getMemberFields()) {
                    if ((_fieldFilter != null) && !_fieldFilter.include(raw)) {
                        continue;
                    }
                    ResolvedField field = fields.get(raw.getName());
                    if (field != null) {
                        for (Annotation ann : raw.getAnnotations()) {
                            if (_annotationHandler.includeMethodAnnotation(ann)) {
                                field.applyOverride(ann);
                            }
                        }
                    }
                }
            } else { // If actual type, add fields, masking whatever might have existed before:
                for (RawField field : thisType.getType().getMemberFields()) {
                    if ((_fieldFilter != null) && !_fieldFilter.include(field)) {
                        continue;
                    }
                    fields.put(field.getName(), resolveField(field));
                }
            }
        }
        // and that's it?
        if (fields.size() == 0) {
            return NO_RESOLVED_FIELDS;
        }
        return fields.values().toArray(new ResolvedField[0]);
    }
```
[x] FasterXML--woodstox--findSymbol
https://github.com/FasterXML/woodstox/blob/98d841d459d2a371c447e45f561b5f642717f4e0/./src/main/java/com/ctc/wstx/util/SymbolTable.java#L356-L438
```
    /*
    ////////////////////////////////////////////////////
    // Public API, accessing symbols:
    ////////////////////////////////////////////////////
     */

    /**
     * Main access method; will check if actual symbol String exists;
     * if so, returns it; if not, will create, add and return it.
     *
     * @return The symbol matching String in input array
     */
    /*
    public String findSymbol(char[] buffer, int start, int len)
    {
        return findSymbol(buffer, start, len, calcHash(buffer, start, len));
    }
    */

    public String findSymbol(char[] buffer, int start, int len, int hash)
    {
        // Sanity check:
        if (len < 1) {
            return EMPTY_STRING;
        }

        hash &= mIndexMask;

        String sym = mSymbols[hash];

        // Optimal case; checking existing primary symbol for hash index:
        if (sym != null) {
            // Let's inline primary String equality checking:
            if (sym.length() == len) {
                int i = 0;
                do {
                    if (sym.charAt(i) != buffer[start+i]) {
                        break;
                    }
                } while (++i < len);
                // Optimal case; primary match found
                if (i == len) {
                    return sym;
                }
            }
            // How about collision bucket?
            Bucket b = mBuckets[hash >> 1];
            if (b != null) {
                sym = b.find(buffer, start, len);
                if (sym != null) {
                    return sym;
                }
            }
        }

        // Need to expand?
        if (mSize >= mSizeThreshold) {
            rehash();
            /* Need to recalc hash; rare occurence (index mask has been
             * recalculated as part of rehash)
             */
            hash = calcHash(buffer, start, len) & mIndexMask;
        } else if (!mDirty) {
            // Or perhaps we need to do copy-on-write?
            copyArrays();
            mDirty = true;
        }
        ++mSize;

        String newSymbol = new String(buffer, start, len);
        if (mInternStrings) {
            newSymbol = newSymbol.intern();
        }
        // Ok; do we need to add primary entry, or a bucket?
        if (mSymbols[hash] == null) {
            mSymbols[hash] = newSymbol;
        } else {
            int bix = hash >> 1;
            mBuckets[bix] = new Bucket(newSymbol, mBuckets[bix]);
        }

        return newSymbol;
    }
```
[ ] FasterXML--woodstox--reset
https://github.com/FasterXML/woodstox/blob/98d841d459d2a371c447e45f561b5f642717f4e0/./src/main/java/com/ctc/wstx/sr/AttributeCollector.java#L217-L251
```
    /**
     * Method called to allow reusing of collector, usually right before
     * starting collecting attributes for a new start tag.
     */
    /**
     * Method called to allow reusing of collector, usually right before
     * starting collecting attributes for a new start tag.
     *<p>
     * Note: public only so that it can be called by unit tests.
     */
    public void reset()
    {
        if (mNsCount > 0) {
            mNamespaceBuilder.reset();
            mDefaultNsDeclared = false;
            mNsCount = 0;
        }

        /* No need to clear attr name, or NS prefix Strings; they are
         * canonicalized and will be referenced by symbol table in any
         * case... so we can save trouble of cleaning them up. This Object
         * will get GC'ed soon enough, after parser itself gets disposed of.
         */
        if (mAttrCount > 0) {
            mValueBuilder.reset();
            mAttrCount = 0;
            if (mXmlIdAttrIndex >= 0) {
                mXmlIdAttrIndex = XMLID_IX_NONE;
            }
        }
        /* Note: attribute values will be cleared later on, when validating
         * namespaces. This so that we know how much to clean up; and
         * occasionally can also just avoid clean up (when resizing)
         */
    }
```
[x] FasterXML--woodstox--unshare
https://github.com/FasterXML/woodstox/blob/98d841d459d2a371c447e45f561b5f642717f4e0/./src/main/java/com/ctc/wstx/util/TextBuffer.java#L1144-L1173
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len > 0) {
            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
[x] KilianB--JImageHash--calcValue
https://github.com/KilianB/JImageHash/blob/c41bd3daca951e9397dff10a6143cfa981069cab/./src/main/java/dev/brachtendorf/jimagehash/hashAlgorithms/filter/Kernel.java#L644-L680
```
	/**
	 * 
	 * @param input array
	 * @param x     pixelToLookAt
	 * @param y     pixelToLookAt
	 * @return convolutedPixel fo this x and y
	 */
	protected double calcValue(double[][] input, int x, int y) {
		double value = 0;
		int maskW = mask[0].length / 2;
		int maskH = mask.length / 2;

		int width = input[0].length;
		int height = input.length;

		for (int yMask = -maskH; yMask <= maskH; yMask++) {
			for (int xMask = -maskW; xMask <= maskW; xMask++) {

				int xPixelIndex;
				int yPixelIndex;

				if (edgeHandling.equals(EdgeHandlingStrategy.NO_OP)) {
					xPixelIndex = x + xMask;
					yPixelIndex = y + yMask;

					if (xPixelIndex < 0 || xPixelIndex >= width || yPixelIndex < 0 || yPixelIndex >= height) {
						return input[y][x];
					}
				} else {
					xPixelIndex = edgeHandling.correctPixel(x + xMask, width);
					yPixelIndex = edgeHandling.correctPixel(y + yMask, height);
				}
				value += mask[yMask + maskH][xMask + maskW] * input[yPixelIndex][xPixelIndex];
			}
		}
		return value;
	}
```
[ ] KilianB--JImageHash--computeDimensions
https://github.com/KilianB/JImageHash/blob/c41bd3daca951e9397dff10a6143cfa981069cab/./src/main/java/dev/brachtendorf/jimagehash/hashAlgorithms/DifferenceHash.java#L144-L169
```
	/**
	 * Compute the dimension for the resize operation. We want to get to close to a
	 * quadratic images as possible to counteract scaling bias.
	 * 
	 * @param bitResolution the desired resolution
	 */
	private void computeDimensions(int bitResolution) {
		int dimension = (int) Math.round(Math.sqrt(bitResolution + 1));

		// width //height
		int normalBound = (dimension - 1) * (dimension);
		int higherBound = (dimension - 1) * (dimension + 1);

		this.width = dimension;
		this.height = dimension;

		if (higherBound < bitResolution) {
			this.width++;
			this.height++;
		} else {
			if (normalBound < bitResolution || (normalBound - bitResolution) > (higherBound - bitResolution)) {
				this.height++;
			}
		}

	}
```
[ ] KilianB--JImageHash--getUncertaintyMask
https://github.com/KilianB/JImageHash/blob/c41bd3daca951e9397dff10a6143cfa981069cab/./src/main/java/dev/brachtendorf/jimagehash/hash/FuzzyHash.java#L613-L644
```
	/**
	 * Return a mask indicating if the bits are above a certain uncertainty.
	 * <p>
	 * The certainty of a hash is calculated by comparing the number of 0 bits at
	 * position n with the number of 1 bits at position n of all the added hashes.
	 * If all hashes agree the certainty is 100%. If 50% of the hashes contain 0
	 * bits and the other half contains 1 bits the bit has a certainty of 0.
	 * 
	 * <p>
	 * Be aware that index 0 relegates to the rightmost bit. Printing the array will
	 * show the boolean values in reverse order.
	 * 
	 * <p>
	 * This method only returns useable results as soon as one hash was added-
	 * 
	 * 
	 * @param certainty the certainty [0-1] up to which bits will be included. In
	 *                  other words, if a bit is more certain than specified by this
	 *                  argument it will not be included in the result.
	 * @return a boolean array indicating which bits are uncertain
	 */
	public boolean[] getUncertaintyMask(double certainty) {

		ensureUpToDateWeights();

		boolean[] uncertainBits = new boolean[getBitResolution()];

		for (int i = 0; i < uncertainBits.length; i++) {
			uncertainBits[i] = !(bitWeights[i] > certainty || bitWeights[i] < -certainty);
		}
		return uncertainBits;
	}
```
[ ] KilianB--JImageHash--weightedDistance
https://github.com/KilianB/JImageHash/blob/c41bd3daca951e9397dff10a6143cfa981069cab/./src/main/java/dev/brachtendorf/jimagehash/hash/FuzzyHash.java#L357-L388
```
	/**
	 * Calculate the normalized weighted distance between the supplied hash and this
	 * hash.
	 * 
	 * Opposed to the hamming distance the weighted distance takes partial bits into
	 * account.
	 * 
	 * e.g. if this fuzzy hashes first bit hash a probability of 70% being a 0 it
	 * will have a weighted distance of .7 if it's a 1.
	 * 
	 * Be aware that this method id much more expensive than calculating the simple
	 * distance between 2 ordinary hashes. (1 quick xor vs multiple calculations per
	 * bit).
	 * 
	 * @param h The hash to calculate the distance to
	 * @return similarity value ranging between [0 - 1]
	 */
	public double weightedDistance(Hash h) {

		ensureUpToDateDistance();

		double hammingDistance = 0;
		for (int bit = hashLength - 1; bit >= 0; bit--) {

			if (h.getBitUnsafe(bit)) {
				hammingDistance += bitDistance[bit];
			} else {
				hammingDistance += 1 - bitDistance[bit];
			}
		}
		return hammingDistance / hashLength;
	}
```
[x] Kludex--starlette--get_endpoints
https://github.com/Kludex/starlette/blob/7e4b7428f273dbdc875dcd036d20804bcfc7b2ee/./starlette/schemas.py#L39-L86
```
    def get_endpoints(self, routes: list[BaseRoute]) -> list[EndpointInfo]:
        """
        Given the routes, yields the following information:

        - path
            eg: /users/
        - http_method
            one of 'get', 'post', 'put', 'patch', 'delete', 'options'
        - func
            method ready to extract the docstring
        """
        endpoints_info: list[EndpointInfo] = []

        for route in routes:
            if isinstance(route, (Mount, Host)):
                routes = route.routes or []
                if isinstance(route, Mount):
                    path = self._remove_converter(route.path)
                else:
                    path = ""
                sub_endpoints = [
                    EndpointInfo(
                        path="".join((path, sub_endpoint.path)),
                        http_method=sub_endpoint.http_method,
                        func=sub_endpoint.func,
                    )
                    for sub_endpoint in self.get_endpoints(routes)
                ]
                endpoints_info.extend(sub_endpoints)

            elif not isinstance(route, Route) or not route.include_in_schema:
                continue

            elif inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint):
                path = self._remove_converter(route.path)
                for method in route.methods or ["GET"]:
                    if method == "HEAD":
                        continue
                    endpoints_info.append(EndpointInfo(path, method.lower(), route.endpoint))
            else:
                path = self._remove_converter(route.path)
                for method in ["get", "post", "put", "patch", "delete", "options"]:
                    if not hasattr(route.endpoint, method):
                        continue
                    func = getattr(route.endpoint, method)
                    endpoints_info.append(EndpointInfo(path, method.lower(), func))

        return endpoints_info
```
[ ] Manevolent--ffmpeg4j--next
https://github.com/Manevolent/ffmpeg4j/blob/4f7db5710c8e0b762e23365fcf5705c26092b23b/./src/main/java/com/github/manevolent/ffmpeg4j/source/MediaSourceSubstream.java#L54-L67
```
    /**
     * Gets the next available object from the source stream.
     * @return Object.  Null, if the substream is otherwise empty or ended.
     * @throws IOException
     */
    public T next() throws IOException {
        while (frameQueue.size() <= 0)
        {
            if (!isDecoding()) throw new IOException(new IllegalStateException("not decoding"));
            read();
        }

        return tryNext();
    }
```
[ ] Mastercard--client-encryption-java--updateHeader-2
https://github.com/Mastercard/client-encryption-java/blob/f91ae60c3de7660fc9d8ce7b38adba751b2ed304/./src/main/java/com/mastercard/developer/utils/FeignUtils.java#L36-L57
```
    /**
     * Update the value of an HTTP response header and return the updated response. Delete the header if the value is null.
     */
    public static Response updateHeader(Response response, String name, String value) {
        if (name == null) {
            // Do nothing
            return response;
        }
        Map<String, Collection<String>> headers = new HashMap<>(response.headers()); // Headers is an UnmodifiableMap
        Set<String> headerNames = new HashSet<>(headers.keySet());
        for (String headerName : headerNames) {
            if (headerName.equalsIgnoreCase(name)) {
                headers.remove(headerName);
            }
        }
        if (value != null) {
            headers.put(name, Collections.singleton(value));
        }
        return response.toBuilder()
                .headers(headers)
                .build();
    }
```
[ ] Mastercard--oauth1-signer-java--getBaseUriString
https://github.com/Mastercard/oauth1-signer-java/blob/8c84f7d0309f2de6a1a93ff5933d588fd861867c/./src/main/java/com/mastercard/developer/oauth/OAuth.java#L201-L228
```
  /**
   * Normalizes the URL as per
   * https://tools.ietf.org/html/rfc5849#section-3.4.1.2
   *
   * @param uri URL that will be called as part of this request
   * @return Normalized URL
   */
  static String getBaseUriString(URI uri) {
    // Lowercase scheme and authority
    String scheme = uri.getScheme().toLowerCase();
    String authority = uri.getAuthority().toLowerCase();

    // Remove port if it matches the default for scheme
    if (("http".equals(scheme) && uri.getPort() == 80)
        || ("https".equals(scheme) && uri.getPort() == 443)) {
      int index = authority.lastIndexOf(':');
      if (index >= 0) {
        authority = authority.substring(0, index);
      }
    }

    String path = uri.getRawPath();
    if (path == null || path.length() <= 0) {
      path = "/";
    }

    return scheme + "://" + authority + path;
  }
```
[ ] RedisGraph--JRedisGraph--prepareProcedure
https://github.com/RedisGraph/JRedisGraph/blob/92ce65875233bb486ded8ddf73d53dbed329ef35/./src/main/java/com/redislabs/redisgraph/impl/Utils.java#L111-L140
```
    /**
     * Prepare and format a procedure call and its arguments
     * @param procedure - procedure to invoke
     * @param args - procedure arguments
     * @param kwargs - procedure output arguments
     * @return formatter procedure call
     */
    public static String prepareProcedure(String procedure, List<String> args  , Map<String, List<String>> kwargs){
        args = args.stream().map( Utils::quoteString).collect(Collectors.toList());
        StringBuilder queryStringBuilder =  new StringBuilder();
        queryStringBuilder.append("CALL ").append(procedure).append('(');
        int i = 0;
        for (; i < args.size() - 1; i++) {
            queryStringBuilder.append(args.get(i)).append(',');
        }
        if (i == args.size()-1) {
            queryStringBuilder.append(args.get(i));
        }
        queryStringBuilder.append(')');
        List<String> kwargsList = kwargs.getOrDefault("y", null);
        if(kwargsList != null){
            i = 0;
            for (; i < kwargsList.size() - 1; i++) {
                queryStringBuilder.append(kwargsList.get(i)).append(',');

            }
            queryStringBuilder.append(kwargsList.get(i));
        }
        return queryStringBuilder.toString();
    }
```
[ ] SavioAndres--BrasilAPI-Java--isbn
https://github.com/SavioAndres/BrasilAPI-Java/blob/22ecf091db04614cb00b681c841b1464552a2970/./src/main/java/br/com/brasilapi/BrasilAPI.java#L464-L492
```
	/**
	 * Sistema internacional de identificação de livros.
	 * 
	 * O código informado pode conter traços (-) e ambos os formatos são aceitos,
	 * sendo eles o obsoleto de 10 dígitos e o atual de 13 dígitos.
	 * 
	 * Lista de provedores separados por vírgula. Se não especificado, será
	 * realizado uma busca em todos os provedores e o que retornar as informações
	 * mais rapidamente será o escolhido.
	 * 
	 * @param isbn Código isbn.
	 * @param providers Array de String. Provedores dos dados. Provedores
	 *                  disponíves: cbl, mercado-editorial, open-library,
	 *                  google-books.
	 * @return {@link ISBN}
	 */
	public static ISBN isbn(String isbn, String[] providers) {
		String providesParameter = "";
		if (providers != null) {
			providesParameter = "?providers=";
			for (String provider : providers) {
				providesParameter += provider + ",";
			}
			providesParameter = providesParameter.substring(0, providesParameter.length() - 1);
		}

		ISBN obj = (ISBN) api(ISBN.class, "isbn/v1/", isbn + providesParameter);
		return obj != null ? (ISBN) obj.clone() : null;
	}
```
[ ] TheAlgorithms--Java--addBinary
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/greedyalgorithms/BinaryAddition.java#L49-L74
```
    /**
     * Adds two binary strings and returns their sum as a binary string.
     * @param a First binary string.
     * @param b Second binary string.
     * @return Binary string representing the sum of the two binary inputs.
     */
    public String addBinary(String a, String b) {
        // Padding the shorter string with leading zeros
        int maxLength = Math.max(a.length(), b.length());
        a = String.join("", Collections.nCopies(maxLength - a.length(), "0")) + a;
        b = String.join("", Collections.nCopies(maxLength - b.length(), "0")) + b;
        StringBuilder result = new StringBuilder();
        char carry = '0';
        // Iterating over the binary strings from the least significant to the most significant bit
        for (int i = maxLength - 1; i >= 0; i--) {
            char sum = sum(a.charAt(i), b.charAt(i), carry);
            carry = carry(a.charAt(i), b.charAt(i), carry);
            result.append(sum);
        }
        // If there's a remaining carry, append it
        if (carry == '1') {
            result.append('1');
        }
        // Reverse the result as we constructed it from the least significant bit
        return result.reverse().toString();
    }
```
[ ] TheAlgorithms--Java--allNonZeroDegreeVerticesWeaklyConnected
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/graph/HierholzerEulerianPath.java#L260-L302
```
    /**
     * Checks weak connectivity (undirected) among vertices that have non-zero degree.
     *
     * @param startNode node to start DFS from (must be a vertex with non-zero degree)
     * @param n number of vertices
     * @param outDegree out-degree array
     * @param inDegree in-degree array
     * @return true if all vertices having non-zero degree belong to a single weak component
     */
    private boolean allNonZeroDegreeVerticesWeaklyConnected(int startNode, int n, int[] outDegree, int[] inDegree) {
        boolean[] visited = new boolean[n];
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(startNode);
        visited[startNode] = true;

        while (!stack.isEmpty()) {
            int u = stack.pop();
            for (int v : graph.getEdges(u)) {
                if (!visited[v]) {
                    visited[v] = true;
                    stack.push(v);
                }
            }
            for (int x = 0; x < n; x++) {
                if (!visited[x]) {
                    for (int y : graph.getEdges(x)) {
                        if (y == u) {
                            visited[x] = true;
                            stack.push(x);
                            break;
                        }
                    }
                }
            }
        }

        for (int i = 0; i < n; i++) {
            if (outDegree[i] + inDegree[i] > 0 && !visited[i]) {
                return false;
            }
        }
        return true;
    }
```
[ ] TheAlgorithms--Java--backtracking
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/backtracking/Combination.java#L40-L66
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
[ ] TheAlgorithms--Java--calculateGravitationalForce
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/physics/Gravitation.java#L21-L50
```
    /**
     * Calculates the gravitational force vector exerted by one body on another.
     *
     * @param m1 Mass of the first body (kg).
     * @param x1 X-position of the first body (m).
     * @param y1 Y-position of the first body (m).
     * @param m2 Mass of the second body (kg).
     * @param x2 X-position of the second body (m).
     * @param y2 Y-position of the second body (m).
     * @return A double array `[fx, fy]` representing the force vector on the second body.
     */
    public static double[] calculateGravitationalForce(double m1, double x1, double y1, double m2, double x2, double y2) {
        double dx = x1 - x2;
        double dy = y1 - y2;
        double distanceSq = dx * dx + dy * dy;

        // If bodies are at the same position, force is zero to avoid division by zero.
        if (distanceSq == 0) {
            return new double[] {0, 0};
        }

        double distance = Math.sqrt(distanceSq);
        double forceMagnitude = GRAVITATIONAL_CONSTANT * m1 * m2 / distanceSq;

        // Calculate the components of the force vector
        double fx = forceMagnitude * (dx / distance);
        double fy = forceMagnitude * (dy / distance);

        return new double[] {fx, fy};
    }
```
[ ] TheAlgorithms--Java--calculateInDegree
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/graphs/KahnsAlgorithm.java#L86-L98
```
    /**
     * Calculates the in-degree of all vertices in the graph. The in-degree is
     * the number of edges directed into a vertex.
     */
    void calculateInDegree() {
        inDegree = new HashMap<>();
        for (E vertex : graph.getVertices()) {
            inDegree.putIfAbsent(vertex, 0);
            for (E adjacent : graph.getAdjacents(vertex)) {
                inDegree.put(adjacent, inDegree.getOrDefault(adjacent, 0) + 1);
            }
        }
    }
```
[ ] TheAlgorithms--Java--canFormTriangle
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/maths/HeronsFormula.java#L37-L51
```
    /**
     * Checks if the given side lengths satisfy the triangle inequality theorem.
     * <p>
     * The triangle inequality theorem states that the sum of any two sides
     * of a triangle must be greater than the third side.
     * </p>
     *
     * @param a the length of the first side
     * @param b the length of the second side
     * @param c the length of the third side
     * @return true if the sides can form a valid triangle, false otherwise
     */
    private static boolean canFormTriangle(final double a, final double b, final double c) {
        return a + b > c && b + c > a && c + a > b;
    }
```
[x] TheAlgorithms--Java--collectResult
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/randomized/KargerMinCut.java#L177-L193
```
        /*
            This is a verbosity method, it's not a part of the core algorithm,
            But it helps us provide more useful output.
        */
        private KargerOutput collectResult(DisjointSetUnion dsu, int cutEdges) {
            Set<Integer> firstIndices = dsu.getAnySet();
            Set<Integer> firstSet = new HashSet<>();
            Set<Integer> secondSet = new HashSet<>();
            for (int i = 0; i < nodes.size(); i++) {
                if (firstIndices.contains(i)) {
                    firstSet.add(nodes.get(i));
                } else {
                    secondSet.add(nodes.get(i));
                }
            }
            return new KargerOutput(firstSet, secondSet, cutEdges);
        }
```
[ ] TheAlgorithms--Java--decrypt-3
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/ciphers/ColumnarTranspositionCipher.java#L69-L84
```
    /**
     * Decrypts a certain encrypted String with the Columnar Transposition
     * Cipher Rule
     *
     * @return a String decrypted with the word encrypted by the Columnar
     * Transposition Cipher Rule
     */
    public static String decrypt() {
        StringBuilder wordDecrypted = new StringBuilder();
        for (int i = 1; i < table.length; i++) {
            for (Object item : table[i]) {
                wordDecrypted.append(item);
            }
        }
        return wordDecrypted.toString().replaceAll(ENCRYPTION_FIELD, "");
    }
```
[ ] TheAlgorithms--Java--delete-8
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/trees/Trie.java#L103-L131
```
    /**
     * Deletes a word from the Trie.
     * <p>
     * The method traverses the Trie to find the word and marks its end flag as
     * false.
     * It returns true if the word was successfully deleted, false if the word
     * wasn't found.
     *
     * @param word The word to be deleted from the Trie.
     * @return true if the word was found and deleted, false if it was not found.
     */
    public boolean delete(String word) {
        TrieNode currentNode = root;
        for (int i = 0; i < word.length(); i++) {
            TrieNode node = currentNode.child.getOrDefault(word.charAt(i), null);
            if (node == null) {
                return false;
            }

            currentNode = node;
        }

        if (currentNode.end) {
            currentNode.end = false;
            return true;
        }

        return false;
    }
```
[ ] TheAlgorithms--Java--detectLoop
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/lists/CreateAndDetectLoop.java#L70-L91
```
    /**
     * Detects the presence of a loop in the linked list using Floyd's cycle-finding
     * algorithm, also known as the "tortoise and hare" method.
     *
     * @param head the head node of the linked list
     * @return true if a loop is detected, false otherwise
     * @see <a href="https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare">
     *     Floyd's Cycle Detection Algorithm</a>
     */
    static boolean detectLoop(Node head) {
        Node sptr = head;
        Node fptr = head;

        while (fptr != null && fptr.next != null) {
            sptr = sptr.next;
            fptr = fptr.next.next;
            if (sptr == fptr) {
                return true;
            }
        }
        return false;
    }
```
[ ] TheAlgorithms--Java--divideMessageWithP
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/others/CRCAlgorithm.java#L117-L168
```
    /**
     * The most significant part of the CRC algorithm. The message is divided by
     * P, so the dividedMessage ArrayList<Integer> is created. If check == true,
     * the dividedMessaage is examined, in order to see if it contains any 1's.
     * If it does, the message is considered to be wrong by the receiver,so the
     * variable wrongMessCaught changes. If it does not, it is accepted, so one
     * of the variables correctMess, wrongMessNotCaught, changes. If check ==
     * false, the diviided Message is added at the end of the ArrayList<integer>
     * message.
     *
     * @param check the variable used to determine, if the message is going to
     * be checked from the receiver if true, it is checked otherwise, it is not
     */
    public void divideMessageWithP(boolean check) {
        ArrayList<Integer> x = new ArrayList<>();
        ArrayList<Integer> k = (ArrayList<Integer>) message.clone();
        if (!check) {
            for (int i = 0; i < p.size() - 1; i++) {
                k.add(0);
            }
        }
        while (!k.isEmpty()) {
            while (x.size() < p.size() && !k.isEmpty()) {
                x.add(k.get(0));
                k.remove(0);
            }
            if (x.size() == p.size()) {
                for (int i = 0; i < p.size(); i++) {
                    if (x.get(i) == p.get(i)) {
                        x.set(i, 0);
                    } else {
                        x.set(i, 1);
                    }
                }
                for (int i = 0; i < x.size() && x.get(i) != 1; i++) {
                    x.remove(0);
                }
            }
        }
        ArrayList<Integer> dividedMessage = (ArrayList<Integer>) x.clone();
        if (!check) {
            message.addAll(dividedMessage);
        } else {
            if (dividedMessage.contains(1) && messageChanged) {
                wrongMessCaught++;
            } else if (!dividedMessage.contains(1) && messageChanged) {
                wrongMessNotCaught++;
            } else if (!messageChanged) {
                correctMess++;
            }
        }
    }
```
[ ] TheAlgorithms--Java--drawLine
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/geometry/WusLine.java#L74-L133
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
[ ] TheAlgorithms--Java--f
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/ciphers/Blowfish.java#L1150-L1167
```
    /*F-function splits the 32-bit input into four 8-bit quarters
         and uses the quarters as input to the S-boxes.
         The S-boxes accept 8-bit input and produce 32-bit output.
         The outputs are added modulo 232 and XORed to produce the final 32-bit output
        */
    private String f(String plainText) {
        String[] a = new String[4];
        String ans = "";
        for (int i = 0; i < 8; i += 2) {
            // column number for S-box is a 8-bit value
            long col = Long.parseUnsignedLong(hexToBin(plainText.substring(i, i + 2)), 2);
            a[i / 2] = sBox[i / 2][(int) col];
        }
        ans = addBin(a[0], a[1]);
        ans = xor(ans, a[2]);
        ans = addBin(ans, a[3]);
        return ans;
    }
```
[ ] TheAlgorithms--Java--fft
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/maths/FFT.java#L178-L220
```
    /**
     * Iterative In-Place Radix-2 Cooley-Tukey Fast Fourier Transform Algorithm
     * with Bit-Reversal. The size of the input signal must be a power of 2. If
     * it isn't then it is padded with zeros and the output FFT will be bigger
     * than the input signal.
     *
     * <p>
     * More info:
     * https://www.algorithm-archive.org/contents/cooley_tukey/cooley_tukey.html
     * https://www.geeksforgeeks.org/iterative-fast-fourier-transformation-polynomial-multiplication/
     * https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
     * https://cp-algorithms.com/algebra/fft.html
     *  @param x The discrete signal which is then converted to the FFT or the
     * IFFT of signal x.
     * @param inverse True if you want to find the inverse FFT.
     * @return
     */
    public static ArrayList<Complex> fft(ArrayList<Complex> x, boolean inverse) {
        /* Pad the signal with zeros if necessary */
        paddingPowerOfTwo(x);
        int n = x.size();
        int log2n = findLog2(n);
        x = fftBitReversal(n, log2n, x);
        int direction = inverse ? -1 : 1;

        /* Main loop of the algorithm */
        for (int len = 2; len <= n; len *= 2) {
            double angle = -2 * Math.PI / len * direction;
            Complex wlen = new Complex(Math.cos(angle), Math.sin(angle));
            for (int i = 0; i < n; i += len) {
                Complex w = new Complex(1, 0);
                for (int j = 0; j < len / 2; j++) {
                    Complex u = x.get(i + j);
                    Complex v = w.multiply(x.get(i + j + len / 2));
                    x.set(i + j, u.add(v));
                    x.set(i + j + len / 2, u.subtract(v));
                    w = w.multiply(wlen);
                }
            }
        }
        x = inverseFFT(n, inverse, x);
        return x;
    }
```
[ ] TheAlgorithms--Java--find-8
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/searches/LinearSearch.java#L21-L36
```
    /**
     * Generic Linear search method
     *
     * @param array List to be searched
     * @param value Key being searched for
     * @return Location of the key
     */
    @Override
    public <T extends Comparable<T>> int find(T[] array, T value) {
        for (int i = 0; i < array.length; i++) {
            if (array[i].compareTo(value) == 0) {
                return i;
            }
        }
        return -1;
    }
```
[ ] TheAlgorithms--Java--findWays
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/dynamicprogramming/DiceThrow.java#L21-L46
```
    /* The main function that returns the number of ways to get sum 'x' with 'n' dice and 'm' with m
     * faces. */
    public static long findWays(int m, int n, int x) {
        /* Create a table to store the results of subproblems.
    One extra row and column are used for simplicity
    (Number of dice is directly used as row index and sum is directly used as column index).
    The entries in 0th row and 0th column are never used. */
        long[][] table = new long[n + 1][x + 1];

        /* Table entries for only one dice */
        for (int j = 1; j <= m && j <= x; j++) {
            table[1][j] = 1;
        }

        /* Fill rest of the entries in table using recursive relation
    i: number of dice, j: sum */
        for (int i = 2; i <= n; i++) {
            for (int j = 1; j <= x; j++) {
                for (int k = 1; k < j && k <= m; k++) {
                    table[i][j] += table[i - 1][j - k];
                }
            }
        }

        return table[n][x];
    }
```
[ ] TheAlgorithms--Java--floor
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/maths/Floor.java#L8-L23
```
    /**
     * Returns the largest (closest to positive infinity)
     *
     * @param number the number
     * @return the largest (closest to positive infinity) of given
     * {@code number}
     */
    public static double floor(double number) {
        if (number - (int) number == 0) {
            return number;
        } else if (number - (int) number > 0) {
            return (int) number;
        } else {
            return (int) number - 1;
        }
    }
```
[ ] TheAlgorithms--Java--integerToRoman
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/conversions/IntegerToRoman.java#L38-L67
```
    /**
     * Converts an integer to its Roman numeral representation.
     * Steps:
     * <ol>
     *     <li>Iterate over the Roman numeral values in descending order</li>
     *     <li>Calculate how many times a numeral fits</li>
     *     <li>Append the corresponding symbol</li>
     *     <li>Subtract the value from the number</li>
     *     <li>Repeat until the number is zero</li>
     *     <li>Return the Roman numeral representation</li>
     * </ol>
     *
     * @param num the integer value to convert (must be greater than 0)
     * @return the Roman numeral representation of the input integer
     *         or an empty string if the input is non-positive
     */
    public static String integerToRoman(int num) {
        if (num <= 0) {
            return "";
        }

        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < ALL_ROMAN_NUMBERS_IN_ARABIC.length; i++) {
            int times = num / ALL_ROMAN_NUMBERS_IN_ARABIC[i];
            builder.append(ALL_ROMAN_NUMBERS[i].repeat(Math.max(0, times)));
            num -= times * ALL_ROMAN_NUMBERS_IN_ARABIC[i];
        }

        return builder.toString();
    }
```
[ ] TheAlgorithms--Java--intersectsBoundingBox
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/trees/QuadTree.java#L47-L56
```
    /**
     * Checks if the bounding box intersects with the other bounding box
     *
     * @param otherBoundingBox The other bounding box
     * @return true if the bounding box intersects with the other bounding box, false otherwise
     */
    public boolean intersectsBoundingBox(BoundingBox otherBoundingBox) {
        return otherBoundingBox.center.x - otherBoundingBox.halfWidth <= center.x + halfWidth && otherBoundingBox.center.x + otherBoundingBox.halfWidth >= center.x - halfWidth && otherBoundingBox.center.y - otherBoundingBox.halfWidth <= center.y + halfWidth
            && otherBoundingBox.center.y + otherBoundingBox.halfWidth >= center.y - halfWidth;
    }
```
[ ] TheAlgorithms--Java--isJaggedMatrix
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/matrix/utils/MatrixUtil.java#L53-L68
```
    /**
     * @brief Checks if the input matrix is a jagged matrix.
     * Jagged matrix is a matrix where the number of columns in each row is not the same.
     *
     * @param matrix The input matrix
     * @return True if the input matrix is a jagged matrix, false otherwise
     */
    private static boolean isJaggedMatrix(double[][] matrix) {
        int numColumns = matrix[0].length;
        for (double[] row : matrix) {
            if (row.length != numColumns) {
                return true;
            }
        }
        return false;
    }
```
[ ] TheAlgorithms--Java--isPlacedCorrectly
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/backtracking/NQueens.java#L93-L110
```
    /**
     * This function checks if queen can be placed at row = rowIndex in column =
     * columnIndex safely
     *
     * @param columns: columns[i] = rowId where queen is placed in ith column.
     * @param rowIndex: row in which queen has to be placed
     * @param columnIndex: column in which queen is being placed
     * @return true: if queen can be placed safely false: otherwise
     */
    private static boolean isPlacedCorrectly(int[] columns, int rowIndex, int columnIndex) {
        for (int i = 0; i < columnIndex; i++) {
            int diff = Math.abs(columns[i] - rowIndex);
            if (diff == 0 || columnIndex - i == diff) {
                return false;
            }
        }
        return true;
    }
```
[ ] TheAlgorithms--Java--jobSequencingWithDeadlines
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/scheduling/JobSchedulingWithDeadline.java#L47-L87
```
    /**
     * Schedules jobs to maximize profit while respecting their deadlines and arrival times.
     *
     * This method sorts the jobs in descending order of profit and attempts
     * to allocate them to time slots that are before or on their deadlines,
     * provided they have arrived. The function returns an array where the first element
     * is the total number of jobs scheduled and the second element is the total profit earned.
     *
     * @param jobs An array of Job objects, each representing a job with an ID, arrival time,
     *             deadline, and profit.
     * @return An array of two integers: the first element is the count of jobs
     *         that were successfully scheduled, and the second element is the
     *         total profit earned from those jobs.
     */
    public static int[] jobSequencingWithDeadlines(Job[] jobs) {
        Arrays.sort(jobs, Comparator.comparingInt(job -> - job.profit));

        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).max().orElse(0);

        int[] timeSlots = new int[maxDeadline];
        Arrays.fill(timeSlots, -1);

        int count = 0;
        int maxProfit = 0;

        // Schedule the jobs
        for (Job job : jobs) {
            if (job.arrivalTime <= job.deadline) {
                for (int i = Math.min(job.deadline - 1, maxDeadline - 1); i >= job.arrivalTime - 1; i--) {
                    if (timeSlots[i] == -1) {
                        timeSlots[i] = job.jobId;
                        count++;
                        maxProfit += job.profit;
                        break;
                    }
                }
            }
        }

        return new int[] {count, maxProfit};
    }
```
[ ] TheAlgorithms--Java--lookup
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/crdt/LWWElementSet.java#L58-L73
```
    /**
     * Checks if an element is in the LWWElementSet. An element is considered present if it exists in
     * the addSet and either does not exist in the removeSet, or its add timestamp is later than any
     * corresponding remove timestamp.
     *
     * @param key The key of the element to be checked.
     * @return {@code true} if the element is present in the set (i.e., its add timestamp is later
     * than its remove timestamp, or it is not in the remove set), {@code false} otherwise (i.e.,
     * the element has been removed or its remove timestamp is later than its add timestamp).
     */
    public boolean lookup(T key) {
        Element<T> inAddSet = addSet.get(key);
        Element<T> inRemoveSet = removeSet.get(key);

        return inAddSet != null && (inRemoveSet == null || inAddSet.timestamp.isAfter(inRemoveSet.timestamp));
    }
```
[ ] TheAlgorithms--Java--majority
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/hashmap/hashing/MajorityElement.java#L19-L42
```
    /**
     * Returns a list of majority element(s) from the given array of integers.
     *
     * @param nums an array of integers
     * @return a list containing the majority element(s); returns an empty list if none exist or input is null/empty
     */
    public static List<Integer> majority(int[] nums) {
        if (nums == null || nums.length == 0) {
            return Collections.emptyList();
        }

        Map<Integer, Integer> numToCount = new HashMap<>();
        for (final var num : nums) {
            numToCount.merge(num, 1, Integer::sum);
        }

        List<Integer> majorityElements = new ArrayList<>();
        for (final var entry : numToCount.entrySet()) {
            if (entry.getValue() >= nums.length / 2) {
                majorityElements.add(entry.getKey());
            }
        }
        return majorityElements;
    }
```
[ ] TheAlgorithms--Java--maxProduct
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/dynamicprogramming/MaximumProductSubarray.java#L23-L57
```
    /**
     * Finds the maximum product of any contiguous subarray in the given array.
     *
     * @param nums an array of integers which may contain positive, negative,
     *             and zero values.
     * @return the maximum product of a contiguous subarray. Returns 0 if the
     *         array is null or empty.
     */
    public static int maxProduct(int[] nums) {
        if (nums == null || nums.length == 0) {
            return 0;
        }

        long maxProduct = nums[0];
        long currentMax = nums[0];
        long currentMin = nums[0];

        for (int i = 1; i < nums.length; i++) {
            // Swap currentMax and currentMin if current number is negative
            if (nums[i] < 0) {
                long temp = currentMax;
                currentMax = currentMin;
                currentMin = temp;
            }

            // Update currentMax and currentMin
            currentMax = Math.max(nums[i], currentMax * nums[i]);
            currentMin = Math.min(nums[i], currentMin * nums[i]);

            // Update global max product
            maxProduct = Math.max(maxProduct, currentMax);
        }

        return (int) maxProduct;
    }
```
[ ] TheAlgorithms--Java--networkFlow
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/graphs/FordFulkerson.java#L20-L74
```
    /**
     * Computes the maximum flow in a flow network using the Ford-Fulkerson algorithm.
     *
     * @param vertexCount the number of vertices in the flow network
     * @param capacity    a 2D array representing the capacity of edges in the network
     * @param flow        a 2D array representing the current flow in the network
     * @param source      the source vertex in the flow network
     * @param sink        the sink vertex in the flow network
     * @return the total maximum flow from the source to the sink
     */
    public static int networkFlow(int vertexCount, int[][] capacity, int[][] flow, int source, int sink) {
        int totalFlow = 0;

        while (true) {
            int[] parent = new int[vertexCount];
            boolean[] visited = new boolean[vertexCount];
            Queue<Integer> queue = new LinkedList<>();

            queue.add(source);
            visited[source] = true;
            parent[source] = -1;

            while (!queue.isEmpty() && !visited[sink]) {
                int current = queue.poll();

                for (int next = 0; next < vertexCount; next++) {
                    if (!visited[next] && capacity[current][next] - flow[current][next] > 0) {
                        queue.add(next);
                        visited[next] = true;
                        parent[next] = current;
                    }
                }
            }

            if (!visited[sink]) {
                break; // No more augmenting paths
            }

            int pathFlow = INF;
            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                pathFlow = Math.min(pathFlow, capacity[u][v] - flow[u][v]);
            }

            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                flow[u][v] += pathFlow;
                flow[v][u] -= pathFlow;
            }

            totalFlow += pathFlow;
        }

        return totalFlow;
    }
```
[ ] TheAlgorithms--Java--numberOfWays
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/dynamicprogramming/ClimbingStairs.java#L25-L54
```
    /**
     * Calculates the no. of distinct ways to climb a staircase with n steps.
     *
     * @param n the no. of steps in the staircase (non-negative integer)
     * @return the no. of distinct ways to climb to the top
     *         - Returns 0 if n is 0 (no steps to climb).
     *         - Returns 1 if n is 1 (only one way to climb).
     *         - For n > 1, it returns the total no. of ways to climb.
     */
    public static int numberOfWays(int n) {

        // Base case: if there are no steps or only one step, return n.
        if (n == 1 || n == 0) {
            return n;
        }

        int prev = 1; // Ways to reach the step before the current one (step 1)
        int curr = 1; // Ways to reach the current step (step 2)
        int next; // Total ways to reach the next step

        for (int i = 2; i <= n; i++) { // step 2 to n
            next = curr + prev;

            // Move the pointers to the next step
            prev = curr;
            curr = next;
        }

        return curr; // Ways to reach the nth step
    }
```
[ ] TheAlgorithms--Java--pascal
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/maths/PascalTriangle.java#L7-L64
```
    /**
     *In mathematics, Pascal's triangle is a triangular array of the binomial coefficients that
     *arises in probability theory, combinatorics, and algebra. In much of the Western world, it is
     *named after the French mathematician Blaise Pascal, although other mathematicians studied it
     *centuries before him in India, Persia, China, Germany, and Italy.
     *
     * The rows of Pascal's triangle are conventionally enumerated starting with row n=0 at the top
     *(the 0th row). The entries in each row are numbered from the left beginning with k=0 and are
     *usually staggered relative to the numbers in the adjacent rows. The triangle may be
     *constructed in the following manner: In row 0 (the topmost row), there is a unique nonzero
     *entry 1. Each entry of each subsequent row is constructed by adding the number above and to
     *the left with the number above and to the right, treating blank entries as 0. For example, the
     *initial number in the first (or any other) row is 1 (the sum of 0 and 1), whereas the numbers
     *1 and 3 in the third row are added to produce the number 4 in the fourth row. *
     *
     *<p>
     *     link:-https://en.wikipedia.org/wiki/Pascal%27s_triangle
     *
     * <p>
     *     Example:-
     *                  1
     *                1   1
     *              1   2   1
     *            1   3   3   1
     *          1   4   6   4   1
     *        1   5  10   10  5   1
     *      1   6  15  20   15  6   1
     *    1   7  21  35   35  21  7   1
     *  1   8  28  56  70   56   28  8   1
     *
     */

    public static int[][] pascal(int n) {
        /*
         * @param arr  An auxiliary array to store generated pascal triangle values
         * @return
         */
        int[][] arr = new int[n][n];
        /*
         * @param line Iterate through every line and print integer(s) in it
         * @param i Represents the column number of the element we are currently on
         */
        for (int line = 0; line < n; line++) {
            /*
             *  @Every line has number of integers equal to line number
             */
            for (int i = 0; i <= line; i++) {
                // First and last values in every row are 1
                if (line == i || i == 0) {
                    arr[line][i] = 1;
                } else {
                    arr[line][i] = arr[line - 1][i - 1] + arr[line - 1][i];
                }
            }
        }

        return arr;
    }
```
[ ] TheAlgorithms--Java--powSum
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/backtracking/PowerSum.java#L15-L28
```
    /**
     * Calculates the number of ways to express the target sum as a sum of Xth powers of unique natural numbers.
     *
     * @param targetSum The target sum to achieve (N in the problem statement)
     * @param power The power to raise natural numbers to (X in the problem statement)
     * @return The number of ways to express the target sum
     */
    public int powSum(int targetSum, int power) {
        // Special case: when both targetSum and power are zero
        if (targetSum == 0 && power == 0) {
            return 1; // by convention, one way to sum to zero: use nothing
        }
        return sumRecursive(targetSum, power, 1, 0);
    }
```
[ ] TheAlgorithms--Java--print
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/matrix/PrintAMatrixInSpiralOrder.java#L19-L76
```
    /**
     * Returns the elements of the given matrix in spiral order.
     *
     * @param matrix the 2D array to traverse in spiral order
     * @param row    the number of rows in the matrix
     * @param col    the number of columns in the matrix
     * @return a list containing the elements of the matrix in spiral order
     *
     *         <p>
     *         Example:
     *
     *         <pre>
     * int[][] matrix = {
     *   {1, 2, 3},
     *   {4, 5, 6},
     *   {7, 8, 9}
     * };
     * print(matrix, 3, 3) returns [1, 2, 3, 6, 9, 8, 7, 4, 5]
     *         </pre>
     *         </p>
     */
    public List<Integer> print(int[][] matrix, int row, int col) {
        // r traverses matrix row wise from first
        int r = 0;
        // c traverses matrix column wise from first
        int c = 0;
        int i;
        List<Integer> result = new ArrayList<>();
        while (r < row && c < col) {
            // print first row of matrix
            for (i = c; i < col; i++) {
                result.add(matrix[r][i]);
            }
            // increase r by one because first row printed
            r++;
            // print last column
            for (i = r; i < row; i++) {
                result.add(matrix[i][col - 1]);
            }
            // decrease col by one because last column has been printed
            col--;
            // print rows from last except printed elements
            if (r < row) {
                for (i = col - 1; i >= c; i--) {
                    result.add(matrix[row - 1][i]);
                }
                row--;
            }
            // print columns from first except printed elements
            if (c < col) {
                for (i = row - 1; i >= r; i--) {
                    result.add(matrix[i][c]);
                }
                c++;
            }
        }
        return result;
    }
```
[ ] TheAlgorithms--Java--reHashTableIncreasesTableSize
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/hashmap/hashing/HashMapCuckooHashing.java#L124-L137
```
    /**
     * Rehashes the current table to a new size (double the current size) and reinserts existing keys.
     */
    public void reHashTableIncreasesTableSize() {
        HashMapCuckooHashing newT = new HashMapCuckooHashing(tableSize * 2);
        for (int i = 0; i < tableSize; i++) {
            if (buckets[i] != null && !Objects.equals(buckets[i], emptySlot)) {
                newT.insertKey2HashTable(this.buckets[i]);
            }
        }
        this.tableSize *= 2;
        this.buckets = newT.buckets;
        this.thresh = (int) (Math.log(tableSize) / Math.log(2)) + 2;
    }
```
[ ] TheAlgorithms--Java--removeByIndex
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/lists/CursorLinkedList.java#L116-L126
```
    /**
     * Removes the element at a specified logical index from the list.
     *
     * @param index the logical index of the element to remove
     */
    public void removeByIndex(int index) {
        if (index >= 0 && index < count) {
            T element = get(index);
            remove(element);
        }
    }
```
[ ] TheAlgorithms--Java--resetBoard
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/backtracking/KnightsTour.java#L44-L59
```
    /**
     * Resets the chess board to its initial state.
     * Initializes the grid with boundary cells marked as -1 and internal cells as 0.
     * Sets the total number of cells the knight needs to visit.
     */
    public static void resetBoard() {
        grid = new int[BASE][BASE];
        total = (BASE - 4) * (BASE - 4);
        for (int r = 0; r < BASE; r++) {
            for (int c = 0; c < BASE; c++) {
                if (r < 2 || r > BASE - 3 || c < 2 || c > BASE - 3) {
                    grid[r][c] = -1; // Mark boundary cells
                }
            }
        }
    }
```
[ ] TheAlgorithms--Java--reweightGraph
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/graphs/JohnsonsAlgorithm.java#L122-L143
```
    /**
     * Reweights the graph using the modified weights computed by Bellman-Ford.
     *
     * @param graph The original graph.
     * @param modifiedWeights The modified weights from Bellman-Ford.
     * @return The reweighted graph.
     */
    public static double[][] reweightGraph(double[][] graph, double[] modifiedWeights) {
        int numVertices = graph.length;
        double[][] reweightedGraph = new double[numVertices][numVertices];

        for (int i = 0; i < numVertices; i++) {
            for (int j = 0; j < numVertices; j++) {
                if (graph[i][j] != 0) {
                    // New weight = original weight + h(u) - h(v)
                    reweightedGraph[i][j] = graph[i][j] + modifiedWeights[i] - modifiedWeights[j];
                }
            }
        }

        return reweightedGraph;
    }
```
[ ] TheAlgorithms--Java--sentinelSort
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/sorts/InsertionSort.java#L44-L73
```
    /**
     * Sentinel sort is a function which on the first step finds the minimal element in the provided
     * array and puts it to the zero position, such a trick gives us an ability to avoid redundant
     * comparisons like `j > 0` and swaps (we can move elements on position right, until we find
     * the right position for the chosen element) on further step.
     *
     * @param array The array to be sorted
     * @param <T>   The type of elements in the array, which must be comparable
     * @return The sorted array
     */
    public <T extends Comparable<T>> T[] sentinelSort(T[] array) {
        if (array == null || array.length <= 1) {
            return array;
        }

        final int minElemIndex = findMinIndex(array);
        SortUtils.swap(array, 0, minElemIndex);

        for (int i = 2; i < array.length; i++) {
            final T currentValue = array[i];
            int j = i;
            while (j > 0 && SortUtils.less(currentValue, array[j - 1])) {
                array[j] = array[j - 1];
                j--;
            }
            array[j] = currentValue;
        }

        return array;
    }
```
[ ] TheAlgorithms--Java--solve-2
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/graphs/TwoSat.java#L149-L190
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
[ ] TheAlgorithms--Java--sum
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/greedyalgorithms/BinaryAddition.java#L9-L28
```
    /**
     * Computes the sum of two binary characters and a carry.
     * @param a First binary character ('0' or '1').
     * @param b Second binary character ('0' or '1').
     * @param carry The carry from the previous operation ('0' or '1').
     * @return The sum as a binary character ('0' or '1').
     */
    public char sum(char a, char b, char carry) {
        int count = 0;
        if (a == '1') {
            count++;
        }
        if (b == '1') {
            count++;
        }
        if (carry == '1') {
            count++;
        }
        return count % 2 == 0 ? '0' : '1';
    }
```
[ ] TheAlgorithms--Java--union
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/graphs/BoruvkaAlgorithm.java#L169-L188
```
    /**
     * Performs the Union operation for Union-Find
     *
     * @param components array of subsets
     * @param x          index of the first subset
     * @param y          index of the second subset
     */
    static void union(Component[] components, final int x, final int y) {
        final int xroot = find(components, x);
        final int yroot = find(components, y);

        if (components[xroot].rank < components[yroot].rank) {
            components[xroot].parent = yroot;
        } else if (components[xroot].rank > components[yroot].rank) {
            components[yroot].parent = xroot;
        } else {
            components[yroot].parent = xroot;
            components[xroot].rank++;
        }
    }
```
[ ] TheAlgorithms--Java--unionSets-2
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/disjointsetunion/DisjointSetUnionBySize.java#L57-L78
```
    /**
     * Merges the sets containing the two given nodes using union by size.
     * The root of the smaller set is attached to the root of the larger set.
     * @param x a node in the first set
     * @param y a node in the second set
     */
    public void unionSets(Node<T> x, Node<T> y) {
        Node<T> rootX = findSet(x);
        Node<T> rootY = findSet(y);

        if (rootX == rootY) {
            return; // They are already in the same set
        }
        // Union by size: attach smaller tree under the larger one
        if (rootX.size < rootY.size) {
            rootX.parent = rootY;
            rootY.size += rootX.size; // update size
        } else {
            rootY.parent = rootX;
            rootX.size += rootY.size; // update size
        }
    }
```
[ ] TheAlgorithms--Java--xPartition
https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/divideandconquer/ClosestPair.java#L77-L102
```
    /**
     * xPartition function: arrange x-axis.
     *
     * @param a (IN Parameter) array of points <br>
     * @param first (IN Parameter) first point <br>
     * @param last (IN Parameter) last point <br>
     * @return pivot index
     */
    public int xPartition(final Location[] a, final int first, final int last) {
        Location pivot = a[last]; // pivot
        int i = first - 1;
        Location temp; // Temporarily store value for position transformation
        for (int j = first; j <= last - 1; j++) {
            if (a[j].x <= pivot.x) { // Less than or less than pivot
                i++;
                temp = a[i]; // array[i] <-> array[j]
                a[i] = a[j];
                a[j] = temp;
            }
        }
        i++;
        temp = a[i]; // array[pivot] <-> array[i]
        a[i] = a[last];
        a[last] = temp;
        return i; // pivot index
    }
```
[ ] TomasTomecek--sen--assemble_rows
https://github.com/TomasTomecek/sen/blob/3a31c949f3732910a1f2e58ef8ee88c4758c1107/./sen/tui/widgets/table.py#L35-L80
```
def assemble_rows(data, max_allowed_lengths=None, dividechars=1,
                  ignore_columns=None):
    """
    :param data: list of lists:
    [["row 1 column 1", "row 1 column 2"],
     ["row 2 column 1", "row 2 column 2"]]
    each item consists of instance of urwid.Text

    :param max_allowed_lengths: dict:
        {col_index: maximum_allowed_length}
    :param ignore_columns: list of ints, indexes which should not be calculated
    """
    rows = []
    max_lengths = {}
    ignore_columns = ignore_columns or []

    # shitty performance, here we go
    # it would be way better to do a single double loop and provide mutable variable
    # FIXME: merge this code with calculate() from above
    for row in data:
        col_index = 0
        for widget in row:
            if col_index in ignore_columns:
                continue
            l = len(widget.text)
            if max_allowed_lengths:
                if col_index in max_allowed_lengths and max_allowed_lengths[col_index] < l:
                    # l is bigger then what is allowed
                    l = max_allowed_lengths[col_index]

            max_lengths.setdefault(col_index, l)
            max_lengths[col_index] = max(l, max_lengths[col_index])
            col_index += 1

    for row in data:
        row_widgets = []
        for idx, item in enumerate(row):
            if idx in ignore_columns:
                row_widgets.append(item)
            else:
                row_widgets.append((max_lengths[idx], item))
        rows.append(
            RowWidget(row_widgets, dividechars=dividechars)
        )

    return rows
```
[ ] TomasTomecek--sen--calculate_max_cols_length
https://github.com/TomasTomecek/sen/blob/3a31c949f3732910a1f2e58ef8ee88c4758c1107/./sen/tui/widgets/table.py#L11-L32
```
def calculate_max_cols_length(table, size):
    """
    :param table: list of lists:

    [["row 1 column 1", "row 1 column 2"],
     ["row 2 column 1", "row 2 column 2"]]

    each item consists of instance of urwid.Text

    :returns dict, {index: width}
    """
    max_cols_lengths = {}

    for row in table:
        col_index = 0
        for idx, widget in enumerate(row.widgets):
            l = widget.pack((size[0], ))[0]
            max_cols_lengths[idx] = max(max_cols_lengths.get(idx, 0), l)
            col_index += 1

    max_cols_lengths.setdefault(0, 1)  # in case table is empty
    return max_cols_lengths
```
[x] TomasTomecek--sen--strip_from_ansi_esc_sequences
https://github.com/TomasTomecek/sen/blob/3a31c949f3732910a1f2e58ef8ee88c4758c1107/./sen/tui/widgets/list/common.py#L23-L42
```
def strip_from_ansi_esc_sequences(text):
    """
    find ANSI escape sequences in text and remove them

    :param text: str
    :return: list, should be passed to ListBox
    """
    # esc[ + values + control character
    # h, l, p commands are complicated, let's ignore them
    seq_regex = r"\x1b\[[0-9;]*[mKJusDCBAfH]"
    regex = re.compile(seq_regex)
    start = 0
    response = ""
    for match in regex.finditer(text):
        end = match.start()
        response += text[start:end]

        start = match.end()
    response += text[start:len(text)]
    return response
```
[ ] Vonage--vonage-java-sdk--getSupportedOutboundMessageTypes
https://github.com/Vonage/vonage-java-sdk/blob/ff6decc126670aac4f6993b71ab126c3e5a7829d/./src/main/java/com/vonage/client/messages/Channel.java#L53-L65
```
	/**
	 * Similar to {@link #getSupportedMessageTypes()} but excludes message types used only for inbound / webhooks.
	 *
	 * @return The Set of message types that this service can send.
	 * @since 7.5.0
	 */
	public Set<MessageType> getSupportedOutboundMessageTypes() {
		return getSupportedMessageTypes().stream().filter(mt -> mt != MessageType.UNSUPPORTED &&
				mt != MessageType.REPLY && mt != MessageType.ORDER &&
				mt != MessageType.CONTACT && mt != MessageType.BUTTON &&
				(this != Channel.RCS || (mt != AUDIO && mt != LOCATION && mt != VCARD))
		).collect(Collectors.toSet());
	}
```
[ ] Zlika--reproducible-build-maven-plugin--of
https://github.com/Zlika/reproducible-build-maven-plugin/blob/d4f29db868ff0d39fabbef06c1fc3bf8179be089/./src/main/java/io/github/zlika/reproducible/PatternFileNameFilter.java#L63-L111
```
    /**
     * Construct a new pattern-based filename filter.
     *
     * @param log        A logger
     * @param includes   The inclusion patterns
     * @param excludes   The exclusion patterns
     * @param extensions The filename extensions to which this filter applies
     *
     * @return A new filter
     */

    public static PatternFileNameFilter of(
            final Log log,
            final List<String> includes,
            final List<String> excludes,
            final List<String> extensions)
    {
        final ArrayList<Pattern> includePatterns =
                new ArrayList<>(includes.size());
        final ArrayList<Pattern> excludePatterns =
                new ArrayList<>(includes.size());

        for (final String include : includes)
        {
            if (include != null)
            {
                final String trimmed = include.trim();
                if (!trimmed.isEmpty())
                {
                    includePatterns.add(Pattern.compile(trimmed));
                }
            }
        }
        for (final String exclude : excludes)
        {
            if (exclude != null)
            {
                final String trimmed = exclude.trim();
                if (!trimmed.isEmpty())
                {
                    excludePatterns.add(Pattern.compile(trimmed));
                }
            }
        }

        return new PatternFileNameFilter(
                log, includePatterns, excludePatterns, extensions
        );
    }
```
[ ] a2aproject--a2a-python--append_artifact_to_task
https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/utils/helpers.py#L51-L110
```
@trace_function()
def append_artifact_to_task(task: Task, event: TaskArtifactUpdateEvent) -> None:
    """Helper method for updating a Task object with new artifact data from an event.

    Handles creating the artifacts list if it doesn't exist, adding new artifacts,
    and appending parts to existing artifacts based on the `append` flag in the event.

    Args:
        task: The `Task` object to modify.
        event: The `TaskArtifactUpdateEvent` containing the artifact data.
    """
    if not task.artifacts:
        task.artifacts = []

    new_artifact_data: Artifact = event.artifact
    artifact_id: str = new_artifact_data.artifact_id
    append_parts: bool = event.append or False

    existing_artifact: Artifact | None = None
    existing_artifact_list_index: int | None = None

    # Find existing artifact by its id
    for i, art in enumerate(task.artifacts):
        if art.artifact_id == artifact_id:
            existing_artifact = art
            existing_artifact_list_index = i
            break

    if not append_parts:
        # This represents the first chunk for this artifact index.
        if existing_artifact_list_index is not None:
            # Replace the existing artifact entirely with the new data
            logger.debug(
                'Replacing artifact at id %s for task %s', artifact_id, task.id
            )
            task.artifacts[existing_artifact_list_index] = new_artifact_data
        else:
            # Append the new artifact since no artifact with this index exists yet
            logger.debug(
                'Adding new artifact with id %s for task %s',
                artifact_id,
                task.id,
            )
            task.artifacts.append(new_artifact_data)
    elif existing_artifact:
        # Append new parts to the existing artifact's part list
        logger.debug(
            'Appending parts to artifact id %s for task %s',
            artifact_id,
            task.id,
        )
        existing_artifact.parts.extend(new_artifact_data.parts)
    else:
        # We received a chunk to append, but we don't have an existing artifact.
        # we will ignore this chunk
        logger.warning(
            'Received append=True for nonexistent artifact index %s in task %s. Ignoring chunk.',
            artifact_id,
            task.id,
        )
```
[ ] a2aproject--a2a-python--are_modalities_compatible
https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/utils/helpers.py#L317-L342
```
def are_modalities_compatible(
    server_output_modes: list[str] | None, client_output_modes: list[str] | None
) -> bool:
    """Checks if server and client output modalities (MIME types) are compatible.

    Modalities are compatible if:
    1. The client specifies no preferred output modes (client_output_modes is None or empty).
    2. The server specifies no supported output modes (server_output_modes is None or empty).
    3. There is at least one common modality between the server's supported list and the client's preferred list.

    Args:
        server_output_modes: A list of MIME types supported by the server/agent for output.
                             Can be None or empty if the server doesn't specify.
        client_output_modes: A list of MIME types preferred by the client for output.
                             Can be None or empty if the client accepts any.

    Returns:
        True if the modalities are compatible, False otherwise.
    """
    if client_output_modes is None or len(client_output_modes) == 0:
        return True

    if server_output_modes is None or len(server_output_modes) == 0:
        return True

    return any(x in server_output_modes for x in client_output_modes)
```
[ ] a2aproject--a2a-python--get_file_parts
https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/utils/parts.py#L39-L48
```
def get_file_parts(parts: list[Part]) -> list[FileWithBytes | FileWithUri]:
    """Extracts file data from all FilePart objects in a list of Parts.

    Args:
        parts: A list of `Part` objects.

    Returns:
        A list of `FileWithBytes` or `FileWithUri` objects containing the file data from any `FilePart` objects found.
    """
    return [part.root.file for part in parts if isinstance(part.root, FilePart)]
```
[ ] a2aproject--a2a-python--get_requested_extensions
https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/extensions/common.py#L7-L18
```
def get_requested_extensions(values: list[str]) -> set[str]:
    """Get the set of requested extensions from an input list.

    This handles the list containing potentially comma-separated values, as
    occurs when using a list in an HTTP header.
    """
    return {
        stripped
        for v in values
        for ext in v.split(',')
        if (stripped := ext.strip())
    }
```
[ ] a2aproject--a2a-python--normalize_large_integers_to_strings
https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/utils/proto_utils.py#L69-L95
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
[ ] a2aproject--a2a-python--routes
https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/server/apps/jsonrpc/starlette_app.py#L95-L148
```
    def routes(
        self,
        agent_card_url: str = AGENT_CARD_WELL_KNOWN_PATH,
        rpc_url: str = DEFAULT_RPC_URL,
        extended_agent_card_url: str = EXTENDED_AGENT_CARD_PATH,
    ) -> list[Route]:
        """Returns the Starlette Routes for handling A2A requests.

        Args:
            agent_card_url: The URL path for the agent card endpoint.
            rpc_url: The URL path for the A2A JSON-RPC endpoint (POST requests).
            extended_agent_card_url: The URL for the authenticated extended agent card endpoint.

        Returns:
            A list of Starlette Route objects.
        """
        app_routes = [
            Route(
                rpc_url,
                self._handle_requests,
                methods=['POST'],
                name='a2a_handler',
            ),
            Route(
                agent_card_url,
                self._handle_get_agent_card,
                methods=['GET'],
                name='agent_card',
            ),
        ]

        if agent_card_url == AGENT_CARD_WELL_KNOWN_PATH:
            # For backward compatibility, serve the agent card at the deprecated path as well.
            # TODO: remove in a future release
            app_routes.append(
                Route(
                    PREV_AGENT_CARD_WELL_KNOWN_PATH,
                    self._handle_get_agent_card,
                    methods=['GET'],
                    name='deprecated_agent_card',
                )
            )

        # TODO: deprecated endpoint to be removed in a future release
        if self.agent_card.supports_authenticated_extended_card:
            app_routes.append(
                Route(
                    extended_agent_card_url,
                    self._handle_get_authenticated_extended_agent_card,
                    methods=['GET'],
                    name='authenticated_extended_agent_card',
                )
            )
        return app_routes
```
[ ] a2aproject--a2a-python--update_with_message
https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/client/client_task_manager.py#L168-L192
```
    def update_with_message(self, message: Message, task: Task) -> Task:
        """Updates a task object adding a new message to its history.

        If the task has a message in its current status, that message is moved
        to the history first.

        Args:
            message: The new `Message` to add to the history.
            task: The `Task` object to update.

        Returns:
            The updated `Task` object (updated in-place).
        """
        if task.status.message:
            if task.history:
                task.history.append(task.status.message)
            else:
                task.history = [task.status.message]
            task.status.message = None
        if task.history:
            task.history.append(message)
        else:
            task.history = [message]
        self._current_task = task
        return task
```
[ ] adamchainz--django-upgrade--defined_enumeration_types
https://github.com/adamchainz/django-upgrade/blob/05589e6da630cc5b9b589e183fa7c81f0b1fbed7/./src/django_upgrade/fixers/model_field_choices.py#L33-L63
```
def defined_enumeration_types(module: ast.Module, up_to_line: int) -> set[str]:
    """
    Return a set of enumeration type class names defined in the given module, up to a line number.
    """
    if module not in module_defined_enumeration_types:
        enum_dict = {}
        from_imports: defaultdict[str, set[str]] = defaultdict(set)
        for node in module.body:
            if (
                isinstance(node, ast.ImportFrom)
                and node.level == 0
                and node.module is not None
            ):
                from_imports[node.module].update(
                    name.name
                    for name in node.names
                    if name.asname is None and name.name != "*"
                )
            elif isinstance(node, ast.ClassDef):
                # Check if the class inherits from one of Django's choice types
                for base in node.bases:
                    if _is_django_choices_type(from_imports, base):
                        enum_dict[node.name] = node.lineno
                        break
        module_defined_enumeration_types[module] = enum_dict

    return {
        name
        for name, line in module_defined_enumeration_types[module].items()
        if line <= up_to_line
    }
```
[ ] adamchainz--django-upgrade--fixup_dedent_tokens
https://github.com/adamchainz/django-upgrade/blob/05589e6da630cc5b9b589e183fa7c81f0b1fbed7/./src/django_upgrade/main.py#L278-L290
```
def fixup_dedent_tokens(tokens: list[Token]) -> None:
    """For whatever reason the DEDENT / UNIMPORTANT_WS tokens are misordered

    | if True:
    |     if True:
    |         pass
    |     else:
    |^    ^- DEDENT
    |+----UNIMPORTANT_WS
    """
    for i, token in enumerate(tokens):
        if token.name == UNIMPORTANT_WS and tokens[i + 1].name == DEDENT:
            tokens[i], tokens[i + 1] = tokens[i + 1], tokens[i]
```
[ ] adamchainz--django-upgrade--migrate_api_args
https://github.com/adamchainz/django-upgrade/blob/05589e6da630cc5b9b589e183fa7c81f0b1fbed7/./src/django_upgrade/fixers/mail_api_kwargs.py#L149-L174
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "UNIMPORTANT_WS",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
[ ] adamchainz--django-upgrade--parse_call_args
https://github.com/adamchainz/django-upgrade/blob/05589e6da630cc5b9b589e183fa7c81f0b1fbed7/./src/django_upgrade/tokens.py#L126-L156
```
def parse_call_args(
    tokens: list[Token],
    i: int,
) -> tuple[list[tuple[int, int]], int]:
    """
    Given the index of the opening bracket of a function call, step through
    and parse its arguments into a list of tuples of start, end indices.
    Return this list plus the position of the token after.
    """
    args = []
    stack = [i]
    i += 1
    arg_start = i

    while stack:
        token = tokens[i]

        if len(stack) == 1 and token.src == ",":
            args.append((arg_start, i))
            arg_start = i + 1
        elif token.src in BRACES:
            stack.append(i)
        elif token.src == BRACES[tokens[stack[-1]].src]:
            stack.pop()
            # if we're at the end, append that argument
            if not stack and tokens_to_src(tokens[arg_start:i]).strip():
                args.append((arg_start, i))

        i += 1

    return args, i
```
[ ] addthis--stream-lib--computeBucketsAndK
https://github.com/addthis/stream-lib/blob/5a3bc87c5314f7771ea3968e9015a3d25536343e/./src/main/java/com/clearspring/analytics/stream/membership/BloomCalculations.java#L102-L137
```
    /**
     * Given a maximum tolerable false positive probability, compute a Bloom
     * specification which will give less than the specified false positive rate,
     * but minimize the number of buckets per element and the number of hash
     * functions used.  Because bandwidth (and therefore total bitvector size)
     * is considered more expensive than computing power, preference is given
     * to minimizing buckets per element rather than number of hash functions.
     *
     * @param maxFalsePosProb The maximum tolerable false positive rate.
     * @return A Bloom Specification which would result in a false positive rate
     * less than specified by the function call.
     */
    public static BloomSpecification computeBucketsAndK(double maxFalsePosProb) {
        // Handle the trivial cases
        if (maxFalsePosProb >= probs[minBuckets][minK]) {
            return new BloomSpecification(2, optKPerBuckets[2]);
        }
        if (maxFalsePosProb < probs[maxBuckets][maxK]) {
            return new BloomSpecification(maxK, maxBuckets);
        }

        // First find the minimal required number of buckets:
        int bucketsPerElement = 2;
        int K = optKPerBuckets[2];
        while (probs[bucketsPerElement][K] > maxFalsePosProb) {
            bucketsPerElement++;
            K = optKPerBuckets[bucketsPerElement];
        }
        // Now that the number of buckets is sufficient, see if we can relax K
        // without losing too much precision.
        while (probs[bucketsPerElement][K - 1] <= maxFalsePosProb) {
            K--;
        }

        return new BloomSpecification(K, bucketsPerElement);
    }
```
[ ] aeturrell--skimpy--_convert_case
https://github.com/aeturrell/skimpy/blob/9cd3ed61e0d7e6d36cada4c6807ea7452a8c14df/./src/skimpy/__init__.py#L965-L1003
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
[ ] aeturrell--skimpy--_simplify_datetimes_in_array
https://github.com/aeturrell/skimpy/blob/9cd3ed61e0d7e6d36cada4c6807ea7452a8c14df/./src/skimpy/__init__.py#L183-L207
```
@typechecked
def _simplify_datetimes_in_array(rows: np.ndarray) -> np.ndarray:
    """Simplifies 2001/01/01 00:00:00 to 2001/01/01.

    Args:
        rows (np.ndarray):  contain summary info, including datetimes

    Returns:
        np.ndarray: rows with any all zero hours/min/sec stripped out
    """
    timestamp_positions = [
        [
            [idx, i]
            for i, j in enumerate(item)
            if isinstance(j, pd._libs.tslibs.timestamps.Timestamp)
        ]
        for idx, item in enumerate(rows)
    ]
    timestamp_pos_list = list(chain.from_iterable(timestamp_positions))
    timestamp_pos_tuples = [tuple(entry) for entry in timestamp_pos_list]
    for entry in timestamp_pos_tuples:
        hour, min, sec = rows[entry].hour, rows[entry].minute, rows[entry].second
        if hour == min == sec == 0:
            rows[entry] = rows[entry].strftime("%Y-%m-%d")
    return rows
```
[ ] aiogram--aiogram--as_line
https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/formatting.py#L603-L619
```
def as_line(*items: NodeType, end: str = "\n", sep: str = "") -> Text:
    """
    Wrap multiple nodes into line with :code:`\\\\n` at the end of line.

    :param items: Text or Any
    :param end: ending of the line, by default is :code:`\\\\n`
    :param sep: separator between items, by default is empty string
    :return: Text
    """
    if sep:
        nodes = []
        for item in items[:-1]:
            nodes.extend([item, sep])
        nodes.extend([items[-1], end])
    else:
        nodes = [*items, end]
    return Text(*nodes)
```
[ ] aiogram--aiogram--check_webapp_signature
https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/web_app.py#L111-L140
```
def check_webapp_signature(token: str, init_data: str) -> bool:
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    :param token: bot Token
    :param init_data: data from frontend to be validated
    :return:
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:  # pragma: no cover
        # Init data is not a valid query string
        return False
    if "hash" not in parsed_data:
        # Hash is not present in init data
        return False
    hash_ = parsed_data.pop("hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256)
    calculated_hash = hmac.new(
        key=secret_key.digest(),
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(calculated_hash, hash_)
```
[ ] aiogram--aiogram--deserialize_telegram_object
https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/serialization.py#L34-L68
```
def deserialize_telegram_object(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> DeserializedTelegramObject:
    """
    Deserialize Telegram Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized Telegram object.
    """
    extends = {}
    if include_api_method_name and isinstance(obj, TelegramMethod):
        extends["method"] = obj.__api_method__

    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode="python", warnings=False)

    # Fake bot is needed to exclude global defaults from the object.
    fake_bot = _get_fake_bot(default=default)

    files: dict[str, InputFile] = {}
    prepared = fake_bot.session.prepare_value(
        obj,
        bot=fake_bot,
        files=files,
        _dumps_json=False,
    )

    if isinstance(prepared, dict):
        prepared.update(extends)
    return DeserializedTelegramObject(data=prepared, files=files)
```
[ ] aiogram--aiogram--extract_flags
https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/dispatcher/flags.py#L89-L100
```
def extract_flags(handler: Union["HandlerObject", dict[str, Any]]) -> dict[str, Any]:
    """
    Extract flags from handler or middleware context data

    :param handler: handler object or data
    :return: dictionary with all handler flags
    """
    if isinstance(handler, dict) and "handler" in handler:
        handler = handler["handler"]
    if hasattr(handler, "flags"):
        return handler.flags
    return {}
```
[ ] aiogram--aiogram--full_name
https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/types/chat.py#L390-L403
```
    @property
    def full_name(self) -> str:
        """Get full name of the Chat.

        For private chat it is first_name + last_name.
        For other chat types it is title.
        """
        if self.title is not None:
            return self.title

        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"

        return f"{self.first_name}"
```
[ ] aiogram--aiogram--get_reversed_mro_unique_attrs_resolver
https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/class_attrs_resolver.py#L30-L48
```
def get_reversed_mro_unique_attrs_resolver(cls: type) -> Generator[tuple[str, Any], None, None]:
    """
    Resolve and yield attributes from the reversed method resolution order (MRO) of a given class.

    This function iterates through the reversed MRO of a class and yields attributes
    that have not yet been encountered. It avoids duplicates by keeping track of
    attribute names that have already been processed.

    :param cls: The class for which the attributes will be resolved.
    :return: A generator yielding tuples containing attribute names and their values.
    """
    known_attrs = set()
    for base in reversed(inspect.getmro(cls)):
        for name, value in base.__dict__.items():
            if name in known_attrs:
                continue

            yield name, value
            known_attrs.add(name)
```
[ ] aiogram--aiogram--get_url
https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/types/message.py#L4362-L4389
```
    def get_url(
        self, force_private: bool = False, include_thread_id: bool = False
    ) -> Optional[str]:
        """
        Returns message URL. Cannot be used in private (one-to-one) chats.
        If chat has a username, returns URL like https://t.me/username/message_id
        Otherwise (or if {force_private} flag is set), returns https://t.me/c/shifted_chat_id/message_id

        :param force_private: if set, a private URL is returned even for a public chat
        :param include_thread_id: if set, adds chat thread id to URL and returns like https://t.me/username/thread_id/message_id
        :return: string with full message URL
        """
        if self.chat.type in ("private", "group"):
            return None

        chat_value = (
            f"c/{self.chat.shifted_id}"
            if not self.chat.username or force_private
            else self.chat.username
        )

        message_id_value = (
            f"{self.message_thread_id}/{self.message_id}"
            if include_thread_id and self.message_thread_id and self.is_topic_message
            else f"{self.message_id}"
        )

        return f"https://t.me/{chat_value}/{message_id_value}"
```
[x] ajanata--PretendYoureXyzzy--candidateGameId
https://github.com/ajanata/PretendYoureXyzzy/blob/ed08e371978529db8a908e266dc1a8add1d37967/./src/main/java/net/socialgamer/cah/data/GameManager.java#L217-L240
```
  /**
   * Try to guess a good candidate for the next game id.
   *
   * @param skip
   *          An id to skip over.
   * @return A guess for the next game id.
   */
  private int candidateGameId(final int skip) {
    synchronized (games) {
      final int maxGames = getMaxGames();
      if (games.size() >= maxGames) {
        return -1;
      }
      for (int i = 0; i < maxGames; i++) {
        if (i == skip) {
          continue;
        }
        if (!games.containsKey(i)) {
          return i;
        }
      }
      return -1;
    }
  }
```
[ ] alibaba--spring-context-support--findAnnotations
https://github.com/alibaba/spring-context-support/blob/184df1c8cd0b4c11e0c582039eddb308e8ef1761/./src/main/java/com/alibaba/spring/util/AnnotationUtils.java#L67-L161
```
    /**
     * Find specified {@link Annotation} type maps from {@link Method}
     *
     * @param method          {@link Method}
     * @param annotationClass {@link Annotation} type
     * @param <A>             {@link Annotation} type
     * @return {@link Annotation} type maps , the {@link ElementType} as key ,
     * the list of {@link Annotation} as value.
     * If {@link Annotation} was annotated on {@link Method}'s parameters{@link ElementType#PARAMETER} ,
     * the associated {@link Annotation} list may contain multiple elements.
     */
    public static <A extends Annotation> Map<ElementType, List<A>> findAnnotations(Method method,
                                                                                   Class<A> annotationClass) {

        Retention retention = annotationClass.getAnnotation(Retention.class);

        RetentionPolicy retentionPolicy = retention.value();

        if (!RetentionPolicy.RUNTIME.equals(retentionPolicy)) {
            return Collections.emptyMap();
        }

        Map<ElementType, List<A>> annotationsMap = new LinkedHashMap<ElementType, List<A>>();

        Target target = annotationClass.getAnnotation(Target.class);

        ElementType[] elementTypes = target.value();


        for (ElementType elementType : elementTypes) {

            List<A> annotationsList = new LinkedList<A>();

            switch (elementType) {

                case PARAMETER:

                    Annotation[][] parameterAnnotations = method.getParameterAnnotations();

                    for (Annotation[] annotations : parameterAnnotations) {

                        for (Annotation annotation : annotations) {

                            if (annotationClass.equals(annotation.annotationType())) {

                                annotationsList.add((A) annotation);

                            }

                        }

                    }

                    break;

                case METHOD:

                    A annotation = findAnnotation(method, annotationClass);

                    if (annotation != null) {

                        annotationsList.add(annotation);

                    }

                    break;

                case TYPE:

                    Class<?> beanType = method.getDeclaringClass();

                    A annotation2 = findAnnotation(beanType, annotationClass);

                    if (annotation2 != null) {

                        annotationsList.add(annotation2);

                    }

                    break;

            }

            if (!annotationsList.isEmpty()) {

                annotationsMap.put(elementType, annotationsList);

            }


        }

        return Collections.unmodifiableMap(annotationsMap);

    }
```
[ ] alibaba--spring-context-support--getFieldValue
https://github.com/alibaba/spring-context-support/blob/184df1c8cd0b4c11e0c582039eddb308e8ef1761/./src/main/java/com/alibaba/spring/util/FieldUtils.java#L47-L86
```
    /**
     * Get {@link Field} Value
     *
     * @param object    {@link Object}
     * @param fieldName field name
     * @param fieldType field type
     * @param <T>       field type
     * @return {@link Field} Value
     */
    public static <T> T getFieldValue(Object object, String fieldName, Class<T> fieldType) {

        T fieldValue = null;

        Field field = ReflectionUtils.findField(object.getClass(), fieldName, fieldType);

        if (field != null) {

            boolean accessible = field.isAccessible();

            try {

                if (!accessible) {
                    ReflectionUtils.makeAccessible(field);
                }

                fieldValue = (T) ReflectionUtils.getField(field, object);

            } finally {

                if (!accessible) {
                    field.setAccessible(accessible);
                }

            }

        }

        return fieldValue;

    }
```
[ ] alibaba--spring-context-support--registerInfrastructureBean
https://github.com/alibaba/spring-context-support/blob/184df1c8cd0b4c11e0c582039eddb308e8ef1761/./src/main/java/com/alibaba/spring/util/BeanRegistrar.java#L46-L73
```
    /**
     * Register Infrastructure Bean
     *
     * @param beanDefinitionRegistry {@link BeanDefinitionRegistry}
     * @param beanType               the type of bean
     * @param beanName               the name of bean
     * @return if it's a first time to register, return <code>true</code>, or <code>false</code>
     */
    public static boolean registerInfrastructureBean(BeanDefinitionRegistry beanDefinitionRegistry,
                                                     String beanName,
                                                     Class<?> beanType) {

        boolean registered = false;

        if (!beanDefinitionRegistry.containsBeanDefinition(beanName)) {
            RootBeanDefinition beanDefinition = new RootBeanDefinition(beanType);
            beanDefinition.setRole(BeanDefinition.ROLE_INFRASTRUCTURE);
            beanDefinitionRegistry.registerBeanDefinition(beanName, beanDefinition);
            registered = true;

            if (log.isInfoEnabled()) {
                log.info("The Infrastructure bean definition [" + beanDefinition
                        + "with name [" + beanName + "] has been registered.");
            }
        }

        return registered;
    }
```
[ ] americanexpress--unify-jdocs--getDifferences
https://github.com/americanexpress/unify-jdocs/blob/325af27be93ae4a1df784cf683cdff61e1bb7ac3/./src/main/java/com/americanexpress/unify/jdocs/JDocument.java#L3491-L3538
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
[x] ammaralii--interview-preparation-kit--solution2
https://github.com/ammaralii/interview-preparation-kit/blob/93dbc402a2b11cfbe9915403532333dcbef233dd/./src/main/java/interviews/amazon/coding_challenge_hackerrank/questions/Question1.java#L49-L69
```
    /**
     * as sorting is happening and java use merge sort so complexity of merge sort is
     * <br/><b>Complexity:</b> O(nlog(n))
     */
    private static int solution2(int[] riceBags) {
        Arrays.sort(riceBags);

        Map<Integer, Integer> riceBagsSetMap = new HashMap<>();
        for (int i = riceBags.length - 1; i >= 0; i--) {
            int product = riceBags[i] * riceBags[i];
            if (riceBagsSetMap.containsKey(product)) {
                int value = riceBagsSetMap.get(product);
                riceBagsSetMap.remove(product);
                riceBagsSetMap.put(riceBags[i], value + 1);
            } else {
                riceBagsSetMap.put(riceBags[i], 1);
            }
        }
        System.out.println(riceBagsSetMap);
        return Collections.max(riceBagsSetMap.entrySet(), Comparator.comparingInt(Map.Entry::getValue)).getValue();
    }
```
[ ] anapaulagomes--pytest-picked--parser-2
https://github.com/anapaulagomes/pytest-picked/blob/6596084633b96664e44b6c48a28dfbf02cd96080/./pytest_picked/modes.py#L102-L133
```
    def parser(self, candidate):
        """
        Discard the first 3 characters.

        Parse affected tests from Unstaged command.
        The command output would look like this:
        A  setup.py
        U tests/test_pytest_picked.py
        ?? .pylintrc
        D  tests/migrations/auto.py
        The first two digits are M, A, D, R, C, U, ? or !
        The third is a white-space and the left is the path of
        the file.
        If the file was deleted it will have a D at the beginning
        of the line. If the file was renamed, it will look like this:
        R  school/migrations/from-school.csv -> new-things-from-school.csv
        Reference:
        https://git-scm.com/docs/git-status#git-status---short
        """
        start_path_index = 3
        rename_indicator = "-> "
        delete_indicator = "D  "
        deleted_and_renamed_indicator = "AD "

        if candidate.startswith(delete_indicator):
            return
        if candidate.startswith(deleted_and_renamed_indicator):
            return
        if rename_indicator in candidate:
            indicator_index = candidate.find(rename_indicator)
            start_path_index = indicator_index + len(rename_indicator)
        return candidate[start_path_index:]
```
[ ] apiflask--apiflask--pagination_builder
https://github.com/apiflask/apiflask/blob/13d2a1b51a7ec68fdcfb9c6250f2db107fcf359a/./src/apiflask/helpers.py#L29-L109
```
def pagination_builder(pagination: PaginationType, **kwargs: t.Any) -> dict:
    """A helper function to make pagination data.

    This function is designed based on Flask-SQLAlchemy's `Pagination` class.
    If you are using a different or custom pagination class, make sure the
    passed pagination object has the following attributes:

    - page
    - per_page
    - pages
    - total
    - next_num
    - has_next
    - prev_num
    - has_prev

    Or you can write your own builder function to build the pagination data.

    Examples:

    ```python
    from apiflask import PaginationSchema, pagination_builder

    ...

    class PetQuery(Schema):
        page = Integer(load_default=1)
        per_page = Integer(load_default=20, validate=Range(max=30))


    class PetsOut(Schema):
        pets = List(Nested(PetOut))
        pagination = Nested(PaginationSchema)


    @app.get('/pets')
    @app.input(PetQuery, location='query')
    @app.output(PetsOut)
    def get_pets(query):
        pagination = PetModel.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        pets = pagination.items
        return {
            'pets': pets,
            'pagination': pagination_builder(pagination)
        }
    ```

    See <https://github.com/apiflask/apiflask/blob/main/examples/pagination/app.py>
    for the complete example.

    Arguments:
        pagination: The pagination object.
        **kwargs: Additional keyword arguments that passed to the
            `url_for` function when generate the page-related URLs.

    *Version Added: 0.6.0*
    """
    endpoint: str | None = request.endpoint
    per_page: int = pagination.per_page

    def get_page_url(page: int) -> str:
        if endpoint is None:  # pragma: no cover
            return ''
        return url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs)

    next: str = get_page_url(pagination.next_num) if pagination.has_next else ''
    prev: str = get_page_url(pagination.prev_num) if pagination.has_prev else ''
    return {
        'total': pagination.total,
        'pages': pagination.pages,
        'per_page': per_page,
        'page': pagination.page,
        'next': next,
        'prev': prev,
        'first': get_page_url(1),
        'last': get_page_url(pagination.pages),
        'current': get_page_url(pagination.page),
    }
```
[ ] ashish-chopra--Structures--printIdenticals
https://github.com/ashish-chopra/Structures/blob/ce0a8f131568368bec3110f4ffddcb74d0b9ca0f/./src/main/java/com/applications/Identicals.java#L28-L52
```
	/**
	 * returns the identical numbers found in
	 * both the sorted array of N integers in running
	 * time of T(N) ~ N for worst case.
	 * 
	 */
	public String printIdenticals() { 
		// instead of printing, we return the list 
		// to compare with expected values
		String list = "[";	
		int i = 0, j = 0;
		while (i < first.length && j < second.length) {
			int result = compare(first[i], second[j]);
			if (result == 0) {
				list += first[i] + ",";
				i++; j++;
			} else if (result == -1) 
				j++;
			else 
				i++;
		}
		list +=  "]";
		System.out.println(list);
		return list;
	}
```
[ ] ashish-chopra--Structures--sink-2
https://github.com/ashish-chopra/Structures/blob/ce0a8f131568368bec3110f4ffddcb74d0b9ca0f/./src/main/java/com/sorting/Heap.java#L106-L121
```
    /*
     * eliminate the violation in the heap in case when a parent key becomes
     * smaller than one or both of is children's using a comparator.
     */
    private static void sink(Comparable[] A, int indice, int len, Comparator c) {
        int j;
        while (indice <= len / 2) {
            j = 2 * indice;
            if ((j < len) && (less(A, j, j + 1, c)))
                j++;
            if (!less(A, indice, j, c))
                break;
            exch(A, indice, j);
            indice = j;
        }
    }
```
[ ] askui--vision-agent--truncate_long_strings
https://github.com/askui/vision-agent/blob/83137b51e4a42cd62474541d4a4fa31240876560/./src/askui/utils/str_utils.py#L33-L73
```
def truncate_long_strings(
    json_data: T,
    max_length: int = 100,
    truncate_length: int = 20,
    tag: str = "[shortened]",
) -> T:
    """
    Traverse and truncate long strings in JSON data.

    Args:
        json_data: The JSON data to process. Can be a dict, list, or str.
        max_length: Maximum length of a string before truncation occurs.
        truncate_length: Number of characters to keep when truncating.
        tag: Tag to append to truncated strings.

    Returns:
        Processed JSON data with truncated long strings. Returns the same type as input.

    Examples:
        >>> truncate_long_strings({"key": "a" * 101})
        {'key': 'aaaaaaaaaaaaaaaaaaaa... [shortened]'}

        >>> truncate_long_strings(["short", "a" * 101])
        ['short', 'aaaaaaaaaaaaaaaaaaaa... [shortened]']

        >>> truncate_long_strings("a" * 101)
        'aaaaaaaaaaaaaaaaaaaa... [shortened]'
    """
    if isinstance(json_data, dict):
        return {
            k: truncate_long_strings(v, max_length, truncate_length, tag)
            for k, v in json_data.items()
        }
    if isinstance(json_data, list):
        return [
            truncate_long_strings(item, max_length, truncate_length, tag)
            for item in json_data
        ]
    if isinstance(json_data, str) and len(json_data) > max_length:
        return f"{json_data[:truncate_length]}... {tag}"
    return json_data
```
[ ] baryhuang--mcp-remote-macos-use--__init__
https://github.com/baryhuang/mcp-remote-macos-use/blob/58c13c785ce76ad1d37975e9b7aa32303b8d7c22/./src/vnc_client.py#L171-L197
```
    def __init__(self, host: str, port: int = 5900, password: Optional[str] = None, username: Optional[str] = None,
                 encryption: str = "prefer_on"):
        """Initialize VNC client with connection parameters.

        Args:
            host: remote MacOs machine hostname or IP address
            port: remote MacOs machine port (default: 5900)
            password: remote MacOs machine password (optional)
            username: remote MacOs machine username (optional, only used with certain authentication methods)
            encryption: Encryption preference, one of "prefer_on", "prefer_off", "server" (default: "prefer_on")
        """
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.encryption = encryption
        self.socket = None
        self.width = 0
        self.height = 0
        self.pixel_format = None
        self.name = ""
        self.protocol_version = ""
        self._last_frame = None  # Store last frame for incremental updates
        self._socket_buffer_size = 8192  # Increased buffer size for better performance
        logger.debug(f"Initialized VNC client for {host}:{port} with encryption={encryption}")
        if username:
            logger.debug(f"Username authentication enabled for: {username}")
```
[ ] beanshell--beanshell--addConstantUtf8Reference
https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/org/objectweb/asm/SymbolTable.java#L843-L866
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value));
    return put(new Entry(constantPoolCount++, tag, value, hashCode));
  }
```
[ ] beanshell--beanshell--put122
https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/org/objectweb/asm/ByteVector.java#L185-L207
```
  /**
   * Puts one byte and two shorts into this byte vector. The byte vector is automatically enlarged
   * if necessary.
   *
   * @param byteValue a byte.
   * @param shortValue1 a short.
   * @param shortValue2 another short.
   * @return this byte vector.
   */
  final ByteVector put122(final int byteValue, final int shortValue1, final int shortValue2) {
    int currentLength = length;
    if (currentLength + 5 > data.length) {
      enlarge(5);
    }
    byte[] currentData = data;
    currentData[currentLength++] = (byte) byteValue;
    currentData[currentLength++] = (byte) (shortValue1 >>> 8);
    currentData[currentLength++] = (byte) shortValue1;
    currentData[currentLength++] = (byte) (shortValue2 >>> 8);
    currentData[currentLength++] = (byte) shortValue2;
    length = currentLength;
    return this;
  }
```
[x] beanshell--beanshell--renderTypeNode
https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/BSHAutoCloseable.java#L69-L90
```
    /** We may not always have a type node (loose typed resources).
     * Then we create the BSHType node and get the type
     * from the BSHVariableDeclarator AllocationExpression nodes. */
    private void renderTypeNode() {
        if (jjtGetNumChildren() == 1) {
            Node tNode = new BSHType(ParserTreeConstants.JJTTYPE);
            Node ambigName = jjtGetChild(0);
            while (ambigName.jjtGetNumChildren() > 0)
                if ((ambigName = ambigName.jjtGetChild(0)) instanceof BSHAmbiguousName)
                    break;
            BSHAmbiguousName ambigNew =
                    new BSHAmbiguousName(ParserTreeConstants.JJTAMBIGUOUSNAME);
            ambigNew.jjtSetParent(tNode);
            ambigNew.text = ((BSHAmbiguousName) ambigName).text;
            tNode.jjtAddChild(ambigNew, 0);
            tNode.jjtSetParent(this);
            Node[] n = new Node[2];
            n[0] = tNode;
            n[1] = children[0];
            children = n;
        }
    }
```
[ ] beanshell--beanshell--searchArchiveForClasses
https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/classpath/BshClassPath.java#L520-L536
```
    /** Search Archive for classes.
     * @param url the archive file location
     * @return array of class names found
     * @throws IOException of any reading problems  */
    static String[] searchArchiveForClasses( URL url ) throws IOException {
        List<String> list = new ArrayList<>();
        ZipInputStream zip = new ZipInputStream(url.openStream());

        ZipEntry ze;
        while( zip.available() == 1 )
            if ( (ze = zip.getNextEntry()) != null
                    && isClassFileName( ze.getName() ) )
                list.add( canonicalizeClassName( ze.getName() ) );
        zip.close();

        return list.toArray( new String[list.size()] );
    }
```
[x] bellshade--Java--binerKeDesimal
https://github.com/bellshade/Java/blob/d5387355d572170808e7ef5d014ec4343e6c3471/./src/main/java/algorithm/conversions/BinaryToDecimal.java#L10-L31
```
  /**
   * fungsi mengubah angka biner ke angka desimal
   * 
   * @param angkaBiner angka biner yang akan dikonversikan
   * @return hasil dari konversi angka biner ke angka desimal
   * @throws IllegalArgumentException ini terjadi jika angka biner tidak terdapat angka 0 atau 1
   */

   public static long binerKeDesimal(long angkaBiner) {
    long valueDesimal = 0;
    long pangkat = 0;
    
    while (angkaBiner != 0) {
      long digit = angkaBiner % 10;
      if (digit > 1) {
        throw new IllegalArgumentException("angka biner tidak benar: " + digit);
      }
      valueDesimal += (long) (digit * Math.pow(BASE_BINER, pangkat++));
      angkaBiner /= 10;
    }
    return valueDesimal;
   }
```
[ ] bottlepy--bottle--_parse_http_header
https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L2920-L2950
```
def _parse_http_header(h):
    """ Parses a typical multi-valued and parametrised HTTP header (e.g. Accept headers) and returns a list of values
        and parameters. For non-standard or broken input, this implementation may return partial results.
    :param h: A header string (e.g. ``text/html,text/plain;q=0.9,*/*;q=0.8``)
    :return: List of (value, params) tuples. The second element is a (possibly empty) dict.
    """
    values = []
    if '"' not in h:  # INFO: Fast path without regexp (~2x faster)
        for value in h.split(','):
            parts = value.split(';')
            values.append((parts[0].strip(), {}))
            for attr in parts[1:]:
                name, value = attr.split('=', 1)
                values[-1][1][name.strip().lower()] = value.strip()
    else:
        lop, key, attrs = ',', None, {}
        for quoted, plain, tok in _hsplit(h):
            value = plain.strip() if plain else quoted.replace('\\"', '"')
            if lop == ',':
                attrs = {}
                values.append((value, attrs))
            elif lop == ';':
                if tok == '=':
                    key = value
                else:
                    attrs[value.strip().lower()] = ''
            elif lop == '=' and key:
                attrs[key.strip().lower()] = value
                key = None
            lop = tok
    return values
```
[ ] bottlepy--bottle--auth
https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L1460-L1472
```
    @property
    def auth(self):
        """ HTTP authentication data as a (user, password) tuple. This
            implementation currently supports basic (not digest) authentication
            only. If the authentication happened at a higher level (e.g. in the
            front web-server or a middleware), the password field is None, but
            the user field is looked up from the ``REMOTE_USER`` environ
            variable. On any errors, None is returned. """
        basic = parse_auth(self.environ.get('HTTP_AUTHORIZATION', ''))
        if basic: return basic
        ruser = self.environ.get('REMOTE_USER')
        if ruser: return (ruser, None)
        return None
```
[ ] bottlepy--bottle--get_cookie
https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L1175-L1191
```
    def get_cookie(self, key, default=None, secret=None, digestmod=hashlib.sha256):
        """ Return the content of a cookie. To read a `Signed Cookie`, the
            `secret` must match the one used to create the cookie (see
            :meth:`Response.set_cookie <BaseResponse.set_cookie>`). If anything goes wrong (missing
            cookie or wrong signature), return a default value. """
        value = self.cookies.get(key)
        if secret:
            # See BaseResponse.set_cookie for details on signed cookies.
            if value and value.startswith('!') and '?' in value:
                sig, msg = map(tob, value[1:].split('?', 1))
                hash = hmac.new(tob(secret), msg, digestmod=digestmod).digest()
                if _lscmp(sig, base64.b64encode(hash)):
                    dst = pickle.loads(base64.b64decode(msg))
                    if dst and dst[0] == key:
                        return dst[1]
            return default
        return value or default
```
[ ] bottlepy--bottle--get_undecorated_callback
https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L531-L550
```
    def get_undecorated_callback(self):
        """ Return the callback. If the callback is a decorated function, try to
            recover the original function. """
        func = self.callback
        while True:
            if getattr(func, '__wrapped__', False):
                func = func.__wrapped__
            elif getattr(func, '__func__', False):
                func = func.__func__
            elif getattr(func, '__closure__', False):
                depr(0, 14, "Decorated callback without __wrapped__",
                     "When applying decorators to route callbacks, make sure"
                     " the decorator uses @functools.wraps or update_wrapper."
                     " This warning may also trigger if you reference callables"
                     " from a nonlocal scope.")
                cells_values = (cell.cell_contents for cell in func.__closure__)
                isfunc = lambda x: isinstance(x, FunctionType) or hasattr(x, '__call__')
                func = next(filter(isfunc, cells_values), func)
            else:
                return func
```
[ ] bottlepy--bottle--params
https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L1217-L1226
```
    @DictProperty('environ', 'bottle.request.params', read_only=True)
    def params(self):
        """ A :class:`FormsDict` with the combined values of :attr:`query` and
            :attr:`forms`. File uploads are stored in :attr:`files`. """
        params = FormsDict()
        for key, value in self.query.allitems():
            params[key] = value
        for key, value in self.forms.allitems():
            params[key] = value
        return params
```
[ ] bottlepy--bottle--path_shift
https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L3037-L3065
```
def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0: return script_name, path_info
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '': pathlist = []
    if scriptlist and scriptlist[0] == '': scriptlist = []
    if 0 < shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif 0 > shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError("Cannot shift. Nothing left from %s" % empty)
    new_script_name = '/' + '/'.join(scriptlist)
    new_path_info = '/' + '/'.join(pathlist)
    if path_info.endswith('/') and pathlist: new_path_info += '/'
    return new_script_name, new_path_info
```
[ ] bottlepy--bottle--remote_route
https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L1474-L1483
```
    @property
    def remote_route(self):
        """ A list of all IPs that were involved in this request, starting with
            the client IP and followed by zero or more proxies. This does only
            work if all proxies support the ```X-Forwarded-For`` header. Note
            that this information can be forged by malicious clients. """
        proxy = self.environ.get('HTTP_X_FORWARDED_FOR')
        if proxy: return [ip.strip() for ip in proxy.split(',')]
        remote = self.environ.get('REMOTE_ADDR')
        return [remote] if remote else []
```
[ ] bottlepy--bottle--uninstall
https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L787-L800
```
    def uninstall(self, plugin):
        """ Uninstall plugins. Pass an instance to remove a specific plugin, a type
            object to remove all plugins that match that type, a string to remove
            all plugins with a matching ``name`` attribute or ``True`` to remove all
            plugins. Return the list of removed plugins. """
        removed, remove = [], plugin
        for i, plugin in list(enumerate(self.plugins))[::-1]:
            if remove is True or remove is plugin or remove is type(plugin) \
               or getattr(plugin, 'name', True) == remove:
                removed.append(plugin)
                del self.plugins[i]
                if hasattr(plugin, 'close'): plugin.close()
        if removed: self.reset()
        return removed
```
[ ] capitalone--datacompy--_get_mismatch_stats
https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/core.py#L709-L764
```
    def _get_mismatch_stats(self, sample_count: int) -> dict:
        """Generate mismatch statistics for the report.

        Parameters
        ----------
        sample_count : int
            Number of samples to include in the report.

        Returns
        -------
        dict
            Dictionary containing mismatch statistics.
        """
        mismatch_stats = []
        match_sample = []
        any_mismatch = False

        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                mismatch_stats.append(
                    {
                        "column": column["column"],
                        "dtype1": column["dtype1"],
                        "dtype2": column["dtype2"],
                        "unequal_cnt": column["unequal_cnt"],
                        "max_diff": column["max_diff"],
                        "null_diff": column["null_diff"],
                        "rel_tol": column["rel_tol"],
                        "abs_tol": column["abs_tol"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            return {
                "mismatch_stats": {
                    "has_mismatches": True,
                    "stats": sorted(mismatch_stats, key=lambda x: x["column"]),
                    "df1_name": self.df1_name,
                    "df2_name": self.df2_name,
                    "samples": [df_to_str(sample) for sample in match_sample],
                    "has_samples": len(match_sample) > 0 and sample_count > 0,
                }
            }
        return {
            "mismatch_stats": {
                "has_mismatches": False,
                "has_samples": False,
            }
        }
```
[ ] capitalone--datacompy--count_matching_rows
https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/core.py#L452-L464
```
    def count_matching_rows(self) -> int:
        """Count the number of rows match (on overlapping fields).

        Returns
        -------
        int
            Number of matching rows
        """
        match_columns = []
        for column in self.intersect_columns():
            if column not in self.join_columns:
                match_columns.append(column + "_match")
        return self.intersect_rows[match_columns].all(axis=1).sum()
```
[ ] capitalone--datacompy--normalize_string_column-2
https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/polars.py#L1104-L1132
```
def normalize_string_column(
    column: pl.Series, ignore_spaces: bool, ignore_case: bool
) -> pl.Series:
    """Normalize a string column by converting to upper case and stripping whitespace.

    Parameters
    ----------
    column : pl.Series
        The column to normalize
    ignore_spaces : bool
        Whether to ignore spaces when normalizing
    ignore_case : bool
        Whether to ignore case when normalizing

    Returns
    -------
    pl.Series
        The normalized column

    Notes
    -----
    Will not operate on categorical columns.
    """
    if str(column.dtype.base_type()) in STRING_TYPE:
        if ignore_spaces:
            column = column.str.strip_chars()
        if ignore_case:
            column = column.str.to_uppercase()
    return column
```
[ ] casbin--jcasbin--addPolicies
https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/model/Policy.java#L221-L237
```
    /**
     * addPolicies adds policy rules to the model.
     *
     * @param sec   the section, "p" or "g".
     * @param ptype the policy type, "p", "p2", .. or "g", "g2", ..
     * @param rules the policy rules.
     * @return succeeds or not.
     */
    public boolean addPolicies(String sec, String ptype, List<List<String>> rules) {
        int size = model.get(sec).get(ptype).policy.size();
        for (List<String> rule : rules) {
            if (!hasPolicy(sec, ptype, rule)) {
                addPolicy(sec, ptype, rule);
            }
        }
        return size < model.get(sec).get(ptype).policy.size();
    }
```
[ ] casbin--jcasbin--buildConditionalRoleLinks
https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/model/Policy.java#L411-L428
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey();
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
[ ] casbin--jcasbin--hasRoleForUser
https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/main/Enforcer.java#L155-L174
```
    /**
     * hasRoleForUser determines whether a user has a role.
     *
     * @param name the user.
     * @param role the role.
     * @return whether the user has the role.
     */
    public boolean hasRoleForUser(String name, String role) {
        List<String> roles = getRolesForUser(name);

        boolean hasRole = false;
        for (String r : roles) {
            if (r.equals(role)) {
                hasRole = true;
                break;
            }
        }

        return hasRole;
    }
```
[ ] casbin--jcasbin--timeMatch
https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/util/BuiltInFunctions.java#L523-L562
```
    /**
     * TimeMatch determines whether the current time is between startTime and endTime.
     * You can use "_" to indicate that the parameter is ignored
     *
     * @param startTime the start time as a string in the format "yyyy-MM-dd HH:mm:ss". Use "_" to ignore the start time.
     * @param endTime the end time as a string in the format "yyyy-MM-dd HH:mm:ss". Use "_" to ignore the end time.
     * @return whether the current time is between startTime and endTime
     */
    public static boolean timeMatch(String startTime, String endTime) {
        LocalDateTime now = LocalDateTime.now();

        if (!startTime.equals("_")) {
            LocalDateTime start;
            // special process for "0000" year,LocalDateTime range is 1-999999999
            if (startTime.startsWith("0000")){
                start = LocalDateTime.MIN;
            }else {
                start = LocalDateTime.parse(startTime, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            }
            if (!now.isAfter(start)) {
                return false;
            }
        }

        if (!endTime.equals("_")) {

            LocalDateTime end;
            // special process for "0000" year,LocalDateTime range is 1-999999999
            if (endTime.startsWith("0000")){
                end = LocalDateTime.MIN;
            }else {
                end = LocalDateTime.parse(endTime, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            }
            if (!now.isBefore(end)) {
                return false;
            }
        }

        return true;
    }
```
[x] chiphuyen--sniffly--_merge_and_deduplicate_streaming
https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/core/processor.py#L834-L877
```
    def _merge_and_deduplicate_streaming(self, messages: list[dict]) -> list[dict]:
        """Combined streaming merge and deduplication for Phase 2 optimization.

        This combines _merge_streaming_messages functionality with deduplication
        in a single pass for better performance.
        """
        # First do the streaming merge exactly like the original
        # Group by message_id
        message_groups = defaultdict(list)

        for msg in messages:
            if msg["type"] == "assistant":
                # Check for message ID in raw data
                msg_id = None
                if msg.get("_raw_data", {}).get("message", {}).get("id"):
                    msg_id = msg["_raw_data"]["message"]["id"]
                elif msg.get("message_id"):
                    msg_id = msg["message_id"]

                if msg_id:
                    msg["message_id"] = msg_id  # Store for easy access
                    message_groups[msg_id].append(msg)

        # Process groups
        merged = []
        processed_ids = set()

        for msg in messages:
            msg_id = msg.get("message_id")

            # Handle grouped assistant messages
            if msg_id and msg["type"] == "assistant" and msg_id in message_groups and len(message_groups[msg_id]) > 1:
                if msg_id not in processed_ids:
                    # Merge the group
                    group = message_groups[msg_id]
                    merged_msg = self._merge_message_group(group)
                    merged.append(merged_msg)
                    processed_ids.add(msg_id)

            # Add non-grouped messages
            elif not (msg_id and msg["type"] == "assistant" and msg_id in processed_ids):
                merged.append(msg)

        return merged
```
[ ] chiphuyen--sniffly--get_all_projects_with_metadata
https://github.com/chiphuyen/sniffly/blob/a237d7e9a9b37181626c049046c99b496f6c33c5/./sniffly/utils/log_finder.py#L117-L173
```
def get_all_projects_with_metadata() -> list[dict]:
    """
    Get all Claude projects with metadata for fast display.

    Returns metadata without reading file contents for performance.

    Returns:
        List of dictionaries containing:
        - dir_name: Directory name in .claude/projects
        - log_path: Full path to log directory
        - file_count: Number of JSONL files
        - total_size_mb: Total size of JSONL files in MB
        - last_modified: Unix timestamp of most recent modification
        - first_seen: Unix timestamp of earliest file (approximation of first use)
        - display_name: Human-readable project name
    """
    projects = []
    claude_base = Path.home() / ".claude" / "projects"

    if not claude_base.exists():
        return projects

    try:
        for log_dir in claude_base.iterdir():
            if log_dir.is_dir():
                jsonl_files = list(log_dir.glob("*.jsonl"))
                if jsonl_files:
                    # Get metadata without reading file contents
                    total_size = sum(f.stat().st_size for f in jsonl_files)

                    # Get modification times
                    mtimes = [f.stat().st_mtime for f in jsonl_files]
                    latest_mtime = max(mtimes)
                    earliest_mtime = min(mtimes)

                    # Use directory name as display name
                    # Don't convert dashes to slashes as we can't distinguish
                    # between dashes that were originally in the name vs path separators
                    dir_name = log_dir.name
                    display_name = dir_name

                    projects.append(
                        {
                            "dir_name": dir_name,
                            "log_path": str(log_dir),
                            "file_count": len(jsonl_files),
                            "total_size_mb": round(total_size / (1024 * 1024), 2),
                            "last_modified": latest_mtime,
                            "first_seen": earliest_mtime,
                            "display_name": display_name,
                        }
                    )
    except Exception as e:
        # Log error but continue - don't fail completely
        logger.info(f"Error reading project metadata: {e}")

    return projects
```
[ ] coderamp-labs--gitingest--_parse_ignore_file
https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/./src/gitingest/utils/ignore_patterns.py#L200-L240
```
def _parse_ignore_file(ignore_file: Path, root: Path) -> set[str]:
    """Parse an ignore file and return a set of ignore patterns.

    Parameters
    ----------
    ignore_file : Path
        The path to the ignore file.
    root : Path
        The root directory of the repository.

    Returns
    -------
    set[str]
        A set of ignore patterns.

    """
    patterns: set[str] = set()

    # Path of the ignore file relative to the repository root
    rel_dir = ignore_file.parent.relative_to(root)
    base_dir = Path() if rel_dir == Path() else rel_dir

    with ignore_file.open(encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):  # comments / blank lines
                continue

            # Handle negation ("!foobar")
            negated = line.startswith("!")
            if negated:
                line = line[1:]

            # Handle leading slash ("/foobar")
            if line.startswith("/"):
                line = line.lstrip("/")

            pattern_body = (base_dir / line).as_posix()
            patterns.add(f"!{pattern_body}" if negated else pattern_body)

    return patterns
```
[ ] cojen--Maker--canConvertTo
https://github.com/cojen/Maker/blob/e2d6d1639ff7abd2d6afce0a63c93bafa076e08a/./src/main/java/org/cojen/maker/BaseType.java#L349-L441
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
[ ] cojen--Maker--finish
https://github.com/cojen/Maker/blob/e2d6d1639ff7abd2d6afce0a63c93bafa076e08a/./src/main/java/org/cojen/maker/ConstantsRegistry.java#L65-L116
```
    /**
     * Called when the class definition is finished, to make the constants loadable.
     *
     * @param lookup can be null if class loader is a ClassInjector.Group.
     */
    static void finish(TheClassMaker cm, MethodHandles.Lookup lookup, Class clazz) {
        Object obj = cm.mExactConstants;
        if (obj == null) {
            return;
        }

        if (obj instanceof Entries entries) {
            entries.prune();
        }

        ClassLoader loader = clazz.getClassLoader();

        if (loader instanceof ClassInjector.Group group) {
            synchronized (group) {
                Map<Class, Object> constants = group.mConstants;
                if (constants == null) {
                    // Use a WeakHashMap because some classes might be hidden and can be
                    // unloaded. A strong reference would prevent this.
                    constants = new WeakHashMap<>(4);
                    group.mConstants = constants;
                }
                constants.put(clazz, obj);
            }
        } else {
            ConstantsRegistry registry;
            synchronized (ConstantsRegistry.class) {
                if (cRegistries == null) {
                    cRegistries = new WeakHashMap<>(4);
                }
                WeakReference<ConstantsRegistry> registryRef = cRegistries.get(loader);
                if (registryRef == null || (registry = registryRef.get()) == null) {
                    registry = defineRegistry(lookup);
                    cRegistries.put(loader, new WeakReference<>(registry));
                }
            }
            synchronized (registry) {
                Map<Class, Object> constants = registry.mConstants;
                if (constants == null) {
                    // Use a WeakHashMap because some classes might be hidden and can be
                    // unloaded. A strong reference would prevent this.
                    constants = new WeakHashMap<>(4);
                    registry.mConstants = constants;
                }
                constants.put(clazz, obj);
            }
        }
    }
```
[x] cojen--Maker--get
https://github.com/cojen/Maker/blob/e2d6d1639ff7abd2d6afce0a63c93bafa076e08a/./src/main/java/org/cojen/maker/WeakCache.java#L39-L59
```
    /**
     * Can be called without explicit synchronization, but entries can appear to go missing.
     * Double check with synchronization.
     */
    public V get(K key) {
        Object ref = poll();
        if (ref != null) {
            synchronized (this) {
                cleanup(ref);
            }
        }

        var entries = mEntries;
        for (var e = entries[key.hashCode() & (entries.length - 1)]; e != null; e = e.mNext) {
            if (e.mKey.equals(key)) {
                return e.get();
            }
        }

        return null;
    }
```
[ ] cojen--Maker--verifyTypes
https://github.com/cojen/Maker/blob/e2d6d1639ff7abd2d6afce0a63c93bafa076e08a/./src/main/java/org/cojen/maker/BaseType.java#L615-L629
```
    /**
     * Verifies that the param types can be assigned by the specific types (if provided).
     * Returns null if assignment isn't allowed, or else return the actual param types to use.
     */
    private static BaseType[] verifyTypes(BaseType[] params, BaseType[] specificParamTypes) {
        if (specificParamTypes != null && params.length == specificParamTypes.length) {
            for (int i=0; i<specificParamTypes.length; i++) {
                if (!specificParamTypes[i].isAssignableFrom(params[i])) {
                    return null;
                }
            }
            return specificParamTypes;
        }
        return params;
    }
```
[ ] cole--aiosmtplib--parse_esmtp_extensions
https://github.com/cole/aiosmtplib/blob/70a849a81c455ba93ba5d704585825879647d5c3/./src/aiosmtplib/esmtp.py#L15-L72
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
[ ] crawler-commons--crawler-commons--getNameVariants
https://github.com/crawler-commons/crawler-commons/blob/d185a090bc29d1eea697cf6ed565dc92258be2a3/./src/main/java/crawlercommons/domains/EffectiveTldFinder.java#L599-L640
```
        /**
         * Generate name variants caused by Internationalized Domain Names:
         * every IDN part of a eTLD can be replaced by its punycoded ASCII
         * variant. For two-part IDN eTLDs this will generate 4 variants.
         *
         * @return set of variant names
         */
        public Set<String> getNameVariants() {
            Set<String> res = new HashSet<>();
            if (idn == null) {
                res.add(domain);
                return res;
            }
            String[] parts = idn.split(DOT_REGEX);
            String[] var = new String[parts.length];
            for (int i = 0; i < parts.length; i++) {
                if (!isAscii(parts[i])) {
                    var[i] = IDN.toASCII(parts[i]);
                }
            }
            for (int i = 0; i < parts.length; i++) {
                Set<String> r = new HashSet<>();
                if (res.size() > 0) {
                    for (String p : res) {
                        r.add(p + DOT + parts[i]);
                    }
                } else {
                    r.add(parts[i]);
                }
                if (var[i] != null && !var[i].equals(parts[i])) {
                    if (res.size() > 0) {
                        for (String p : res) {
                            r.add(p + DOT + var[i]);
                        }
                    } else {
                        r.add(var[i]);
                    }
                }
                res = r;
            }
            return res;
        }
```
[x] crawler-commons--crawler-commons--initialize
https://github.com/crawler-commons/crawler-commons/blob/d185a090bc29d1eea697cf6ed565dc92258be2a3/./src/main/java/crawlercommons/domains/EffectiveTldFinder.java#L156-L224
```
    /**
     * (Re)initialize EffectiveTldFinder with custom public suffix list.
     *
     * @param effectiveTldDataStream
     *            content of public suffix list as input stream
     * @return true if (re)initialization was successful
     */
    public boolean initialize(InputStream effectiveTldDataStream) {
        domains = new HashMap<>();
        domainTrie = new SuffixTrie<>();
        boolean inPrivateDomainSection = false;
        try {
            int linesRead = 0, rulesRead = 0;
            BoundedInputStream isCounting = BoundedInputStream.builder().setInputStream(effectiveTldDataStream).get();
            InputStream is = isCounting;
            List<MessageDigest> digests = new ArrayList<>();
            try {
                MessageDigest md5 = MessageDigest.getInstance("MD5");
                is = new DigestInputStream(is, md5);
                digests.add(md5);
                MessageDigest sha512 = MessageDigest.getInstance("SHA-512");
                is = new DigestInputStream(is, sha512);
                digests.add(sha512);
            } catch (NoSuchAlgorithmException e) {
                LOGGER.warn("Failed to initialize digesting input streams", e);
            }
            BufferedReader input = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8));
            String line = null;
            while (null != (line = input.readLine())) {
                linesRead++;
                if (line.trim().isEmpty()) {
                    continue;
                } else if (line.startsWith(COMMENT)) {
                    if (line.contains("===BEGIN PRIVATE DOMAINS===")) {
                        inPrivateDomainSection = true;
                    } else if (line.contains("===END PRIVATE DOMAINS===")) {
                        inPrivateDomainSection = false;
                    } else {
                        Matcher m = VERSION_PATTERN.matcher(line);
                        if (m.matches()) {
                            LOGGER.info("Public suffix list {}: {}", m.group(1), m.group(2));
                        }
                    }
                    continue;
                }
                rulesRead++;
                EffectiveTLD entry = new EffectiveTLD(line, inPrivateDomainSection);
                for (String var : entry.getNameVariants()) {
                    domains.put(var, entry);
                    domainTrie.put(var, entry);
                }
            }
            configured = true;

            is.close();
            long bytesRead = isCounting.getCount();
            LOGGER.info("Successfully read public suffix list: {} bytes, {} lines, {} rules", bytesRead, linesRead, rulesRead);
            for (MessageDigest digest : digests) {
                byte[] d = digest.digest();
                BigInteger bi = new BigInteger(1, d);
                String hexDigest = String.format(Locale.ROOT, "%0" + (d.length << 1) + "X", bi);
                LOGGER.info("Digest of public suffix list: {} = {}", digest.getAlgorithm(), hexDigest);
            }
        } catch (IOException e) {
            LOGGER.error("EffectiveTldFinder configuration failed: ", e);
            configured = false;
        }
        return configured;
    }
```
[ ] crawler-commons--crawler-commons--isWhitespace
https://github.com/crawler-commons/crawler-commons/blob/d185a090bc29d1eea697cf6ed565dc92258be2a3/./src/main/java/crawlercommons/sitemaps/sax/DelegatorHandler.java#L259-L265
```
    /**
     * Check whether character is any Unicode whitespace, including the space
     * characters not covered by {@link Character#isWhitespace(char)}
     */
    public static boolean isWhitespace(char c) {
        return Character.isWhitespace(c) || c == '\u00a0' || c == '\u2007' || c == '\u202f';
    }
```
[ ] crawler-commons--crawler-commons--normalizeRSSTimestamp
https://github.com/crawler-commons/crawler-commons/blob/d185a090bc29d1eea697cf6ed565dc92258be2a3/./src/main/java/crawlercommons/sitemaps/AbstractSiteMap.java#L232-L251
```
    /**
     * Converts pubDate of RSS to the ISO-8601 instant format, e.g.,
     * '2017-01-05T12:34:54Z' in UTC / GMT time zone, see
     * {@link DateTimeFormatter#ISO_INSTANT}.
     * 
     * @param pubDate
     *            - date time of pubDate in RFC822
     * @return converted to &quot;yyyy-MM-dd'T'HH:mm:ssZ&quot; format or
     *         original value if it doesn't follow the RFC822
     */
    public static String normalizeRSSTimestamp(String pubDate) {
        if (pubDate == null) {
            return null;
        }
        ZonedDateTime zdt = parseRSSTimestamp(pubDate);
        if (zdt == null) {
            return pubDate;
        }
        return W3C_FULLDATE_FORMATTER_UTC.format(zdt);
    }
```
[ ] crawler-commons--crawler-commons--unescapePath
https://github.com/crawler-commons/crawler-commons/blob/d185a090bc29d1eea697cf6ed565dc92258be2a3/./src/main/java/crawlercommons/filters/basic/BasicURLNormalizer.java#L504-L545
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
[ ] d0c-s4vage--lookatme--parse_meta
https://github.com/d0c-s4vage/lookatme/blob/c05abe1804d93254e9139039937eed43fb6b49ab/./lookatme/parser.py#L201-L264
```
    @tutor(
        "general",
        "metadata",
        r"""
        The YAML metadata that can be prefixed in slides includes these top level
        fields:

        ```yaml
        ---
        title: "title"
        date: "date"
        author: "author"
        extensions:
          - extension 1
          # .. list of extensions
        styles:
          # .. nested style fields ..
        ---
        ```

        > **NOTE** The `styles` field will be explained in detail with each markdown
        > element.
        """,
        order=3,
    )
    def parse_meta(self, input_data) -> Tuple[AnyStr, Dict]:
        """Parse the PresentationMeta out of the input data

        :param str input_data: The input data string
        :returns: tuple of (remaining_data, meta)
        """
        found_first = False
        yaml_data = []
        skipped_chars = 0
        for line in input_data.split("\n"):
            skipped_chars += len(line) + 1
            stripped_line = line.strip()

            is_marker = (re.match(r'----*', stripped_line) is not None)
            if is_marker:
                if not found_first:
                    found_first = True
                # found the second one
                else:
                    break

            if found_first and not is_marker:
                yaml_data.append(line)
                continue

            # there was no ----* marker
            if not found_first and stripped_line != "":
                break

        if not found_first:
            return input_data, MetaSchema().load_partial_styles({}, partial=True)

        new_input = input_data[skipped_chars:]
        if len(yaml_data) == 0:
            return new_input, MetaSchema().load_partial_styles({}, partial=True)

        yaml_data = "\n".join(yaml_data)
        data = MetaSchema().loads_partial_styles(yaml_data, partial=True)
        return new_input, data
```
[ ] daavoo--pyntcloud--__init__-2
https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/structures/voxelgrid.py#L18-L66
```
    def __init__(
        self,
        *,
        points,
        colors=None,
        n_x=1,
        n_y=1,
        n_z=1,
        size_x=None,
        size_y=None,
        size_z=None,
        regular_bounding_box=True,
    ):
        """Grid of voxels with support for different build methods.

        Parameters
        ----------
        points: (N, 3) numpy.array
        colors: (N, 3) numpy.array, optional
            Default None.
            If not None, color for each voxel will be computed.
        n_x, n_y, n_z :  int, optional
            Default: 1
            The number of segments in which each axis will be divided.
            Ignored if corresponding size_x, size_y or size_z is not None.
        size_x, size_y, size_z : float, optional
            Default: None
            The desired voxel size along each axis.
            If not None, the corresponding n_x, n_y or n_z will be ignored.
        regular_bounding_box : bool, optional
            Default: True
            If True, the bounding box of the point cloud will be adjusted
            in order to have all the dimensions of equal length.
        """
        super().__init__(points=points)
        self.colors = colors
        self.x_y_z = np.asarray([n_x, n_y, n_z])
        self.sizes = np.asarray([size_x, size_y, size_z])
        self.regular_bounding_box = regular_bounding_box

        self.id = None
        self.xyzmin, self.xyzmax = None, None
        self.segments = None
        self.shape = None
        self.n_voxels = None
        self.voxel_x, self.voxel_y, self.voxel_z = None, None, None
        self.voxel_n = None
        self.voxel_centers = None
        self.voxel_colors = None
```
[ ] daavoo--pyntcloud--cartesian
https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/utils/array.py#L4-L50
```
def cartesian(arrays, out=None):
    """Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """
    arrays = [np.asarray(x) for x in arrays]
    shape = (len(x) for x in arrays)
    dtype = arrays[0].dtype

    ix = np.indices(shape)
    ix = ix.reshape(len(arrays), -1).T

    if out is None:
        out = np.empty_like(ix, dtype=dtype)

    for n, arr in enumerate(arrays):
        out[:, n] = arrays[n][ix[:, n]]

    return out
```
[ ] daavoo--pyntcloud--cartesian_to_spherical
https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/geometry/coord_systems.py#L46-L80
```
def cartesian_to_spherical(xyz, degrees=True):
    """
    Convert cartesian coordinates (x, y, z) to spherical (r, theta, phi).

    Parameters
    ----------
    xyz: (N, 3) ndarray
        Corresponding cartesian coordinates.
    degrees: bool, optional
        If True, azimuthal and polar will be returned in degrees.

    Returns
    -------
    radius: (N,) ndarray
        Radial distance.
    inclination: (N,) ndarray
        Polar angle.
    azimuth: (N,) ndarray
        Azimuthal angle.
    """
    x = xyz[:, 0]
    y = xyz[:, 1]
    z = xyz[:, 2]

    radius = np.nan_to_num(np.sqrt((x * x) + (y * y) + (z * z)))

    inclination = np.nan_to_num(np.arccos(z / radius))

    azimuth = np.nan_to_num(np.arctan2(y, x))

    if degrees:
        inclination = np.rad2deg(inclination)
        azimuth = np.rad2deg(azimuth)

    return radius, inclination, azimuth
```
[ ] daavoo--pyntcloud--describe_element
https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/io/ply.py#L258-L282
```
def describe_element(name, df):
    """Takes the columns of the dataframe and builds a ply-like description

    Parameters
    ----------
    name: str
    df: pandas DataFrame

    Returns
    -------
    element: list[str]
    """
    property_formats = {"f": "float", "u": "uchar", "i": "int", "b": "bool"}
    element = ["element " + name + " " + str(len(df))]

    if name == "face":
        element.append("property list uchar int vertex_indices")

    else:
        for i in range(len(df.columns)):
            # get first letter of dtype to infer format
            f = property_formats[str(df.dtypes[i])[0]]
            element.append("property " + f + " " + df.columns.values[i])

    return element
```
[ ] daavoo--pyntcloud--get_mesh_vertices
https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/core_class.py#L612-L632
```
    def get_mesh_vertices(self, rgb=False, normals=False):
        """Decompose triangles of self.mesh from vertices in self.points.

        Returns
        -------
        v1, v2, v3: ndarray
            (N, 3) arrays of vertices so v1[i], v2[i], v3[i] represent the ith triangle
        """
        use_columns = ["x", "y", "z"]
        if rgb:
            use_columns.extend(["red", "green", "blue"])
        if normals:
            use_columns.extend(["nx", "ny", "nz"])

        points = self.points[use_columns].values

        v1 = points[self.mesh["v1"].values]
        v2 = points[self.mesh["v2"].values]
        v3 = points[self.mesh["v3"].values]

        return v1, v2, v3
```
[ ] daavoo--pyntcloud--write_npz
https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/io/npz.py#L27-L46
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, **kwargs)
    return True
```
[ ] dashjoin--jsonata-java--hofFuncArgs
https://github.com/dashjoin/jsonata-java/blob/0645e7bc78d34ad1afcb67731b57e433b788cd1f/./src/main/java/com/dashjoin/jsonata/Functions.java#L1532-L1552
```
    /**
     * Helper function to build the arguments to be supplied to the function arg of the
     * HOFs map, filter, each, sift and single
     * @param {function} func - the function to be invoked
     * @param {*} arg1 - the first (required) arg - the value
     * @param {*} arg2 - the second (optional) arg - the position (index or key)
     * @param {*} arg3 - the third (optional) arg - the whole structure (array or object)
     * @returns {*[]} the argument list
     */
    public static List hofFuncArgs(Object func, Object arg1, Object arg2, Object arg3) {
        List func_args = new ArrayList<>(); func_args.add(arg1); // the first arg (the value) is required
        // the other two are optional - only supply it if the function can take it
        var length = getFunctionArity(func);
        if (length >= 2) {
            func_args.add(arg2);
        }
        if (length >= 3) {
            func_args.add(arg3);
        }
        return func_args;
    }
```
[ ] dbcli--litecli--find_prev_keyword
https://github.com/dbcli/litecli/blob/c072661298bc52b10c11e6571cc741a6d41360a7/./litecli/packages/parseutils.py#L169-L200
```
def find_prev_keyword(sql):
    """Find the last sql keyword in an SQL statement

    Returns the value of the last keyword, and the text of the query with
    everything after the last keyword stripped
    """
    if not sql.strip():
        return None, ""

    parsed = sqlparse.parse(sql)[0]
    flattened = list(parsed.flatten())

    logical_operators = ("AND", "OR", "NOT", "BETWEEN")

    for t in reversed(flattened):
        if t.value == "(" or (t.is_keyword and (t.value.upper() not in logical_operators)):
            # Find the location of token t in the original parsed statement
            # We can't use parsed.token_index(t) because t may be a child token
            # inside a TokenList, in which case token_index thows an error
            # Minimal example:
            #   p = sqlparse.parse('select * from foo where bar')
            #   t = list(p.flatten())[-3]  # The "Where" token
            #   p.token_index(t)  # Throws ValueError: not in list
            idx = flattened.index(t)

            # Combine the string values of all tokens in the original list
            # up to and including the target keyword token t, to produce a
            # query string with everything after the keyword token removed
            text = "".join(tok.value for tok in flattened[: idx + 1])
            return t, text

    return None, ""
```
[ ] dbcli--litecli--last_word
https://github.com/dbcli/litecli/blob/c072661298bc52b10c11e6571cc741a6d41360a7/./litecli/packages/parseutils.py#L19-L62
```
def last_word(text, include="alphanum_underscore"):
    R"""
    Find the last word in a sentence.

    >>> last_word('abc')
    'abc'
    >>> last_word(' abc')
    'abc'
    >>> last_word('')
    ''
    >>> last_word(' ')
    ''
    >>> last_word('abc ')
    ''
    >>> last_word('abc def')
    'def'
    >>> last_word('abc def ')
    ''
    >>> last_word('abc def;')
    ''
    >>> last_word('bac $def')
    'def'
    >>> last_word('bac $def', include='most_punctuations')
    '$def'
    >>> last_word('bac \def', include='most_punctuations')
    '\\def'
    >>> last_word('bac \def;', include='most_punctuations')
    '\\def;'
    >>> last_word('bac::def', include='most_punctuations')
    'def'
    """

    if not text:  # Empty string
        return ""

    if text[-1].isspace():
        return ""
    else:
        regex = cleanup_regex[include]
        matches = regex.search(text)
        if matches:
            return matches.group(0)
        else:
            return ""
```
[x] dbcli--litecli--output
https://github.com/dbcli/litecli/blob/c072661298bc52b10c11e6571cc741a6d41360a7/./litecli/main.py#L671-L722
```
    def output(self, output, status=None):
        """Output text to stdout or a pager command.

        The status text is not outputted to pager or files.

        The message will be logged in the audit log, if enabled. The
        message will be written to the tee file, if enabled. The
        message will be written to the output file, if enabled.

        """
        if output:
            size = self.prompt_app.output.get_size()

            margin = self.get_output_margin(status)

            fits = True
            buf = []
            output_via_pager = self.explicit_pager and special.is_pager_enabled()
            for i, line in enumerate(output, 1):
                self.log_output(line)
                special.write_tee(line)
                special.write_once(line)
                special.write_pipe_once(line)

                if fits or output_via_pager:
                    # buffering
                    buf.append(line)
                    if len(line) > size.columns or i > (size.rows - margin):
                        fits = False
                        if not self.explicit_pager and special.is_pager_enabled():
                            # doesn't fit, use pager
                            output_via_pager = True

                        if not output_via_pager:
                            # doesn't fit, flush buffer
                            for line in buf:
                                click.secho(line)
                            buf = []
                else:
                    click.secho(line)

            if buf:
                if output_via_pager:
                    # sadly click.echo_via_pager doesn't accept generators
                    click.echo_via_pager("\n".join(buf))
                else:
                    for line in buf:
                        click.secho(line)

        if status:
            self.log_output(status)
            click.secho(status)
```
[x] dbcli--litecli--parse_path
https://github.com/dbcli/litecli/blob/c072661298bc52b10c11e6571cc741a6d41360a7/./litecli/packages/filepaths.py#L39-L52
```
def parse_path(root_dir):
    """Split path into head and last component for the completer.

    Also return position where last component starts.

    :param root_dir: str path
    :return: tuple of (string, string, int)

    """
    base_dir, last_dir, position = "", "", 0
    if root_dir:
        base_dir, last_dir = os.path.split(root_dir)
        position = -len(last_dir) if last_dir else 0
    return base_dir, last_dir, position
```
[ ] dbcli--pgcli--generate_alias
https://github.com/dbcli/pgcli/blob/f46d8446a34084cc2532041619d1f08bda7213e7/./pgcli/pgcompleter.py#L62-L77
```
def generate_alias(tbl, alias_map=None):
    """Generate a table alias.

    Given a table name will return an alias for that table using the first of
    the following options there's a match for.

        1. The predefined alias for table defined in the alias_map.
        2. All upper-case letters in the table name.
        3. The first letter of the table name and all letters preceded by _

    :param tbl: unescaped name of the table to alias
    :param alias_map: optional mapping of predefined table aliases
    """
    if alias_map and tbl in alias_map:
        return alias_map[tbl]
    return "".join([l for l in tbl if l.isupper()] or [l for l, prev in zip(tbl, "_" + tbl) if prev == "_" and l != "_"])
```
[ ] dbcli--pgcli--skip_initial_comment
https://github.com/dbcli/pgcli/blob/f46d8446a34084cc2532041619d1f08bda7213e7/./pgcli/config.py#L76-L98
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
[ ] decorators-squad--eo-yaml--compareTo
https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/BaseScalar.java#L82-L115
```
    /**
     * Compare this Scalar to another node.<br><br>
     *
     * A Scalar is always considered less than a Sequence or a Mapping.<br>
     * If o is Scalar then their String values are compared lexicographically
     *
     * @param other The other AbstractNode.
     * @return
     *  a value < 0 if this < o <br>
     *   0 if this == o or <br>
     *  a value > 0 if this > o
     */
    @Override
    public int compareTo(final YamlNode other) {
        int result = -1;
        if (this == other) {
            result = 0;
        } else if (other == null) {
            result = 1;
        } else if (other instanceof Scalar) {
            final String value = this.value();
            final String otherVal = ((Scalar) other).value();
            if(value == null && otherVal == null) {
                result = 0;
            } else if(value != null && otherVal == null) {
                result = 1;
            } else if (value == null) {
                result = -1;
            } else {
                result = value.compareTo(otherVal);
            }
        }
        return result;
    }
```
[ ] decorators-squad--eo-yaml--mappingOrSequenceStartsAtDash
https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/RtYamlInput.java#L197-L217
```
    /**
     * Is the <i>key:value</i> on the same line as the same sequence marker
     * <i>-</i> ?.
     * <br/>
     * Example:
     * <br/>
     * <code>
     *     - foo: bar
     * </code>
     * @param line Line.
     * @return Boolean.
     */
    private boolean mappingOrSequenceStartsAtDash(final String line){
        //line without indentation.
        final String trimmed = line.trim();
        final boolean escapedScalar = trimmed.matches("^\\s*-\\s*\".*\"$")
            || trimmed.matches("^\\s*-\\s*'.*'$");
        return (trimmed.matches("^\\s*-.+:\\s.*$")
            || trimmed.matches("^\\s*-.+-\\s.*$"))
            && !escapedScalar;
    }
```
[ ] decorators-squad--eo-yaml--recursiveMerge
https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/extensions/MergedYamlMapping.java#L163-L236
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
[ ] decorators-squad--eo-yaml--requireNestedIndentation
https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/YamlLine.java#L146-L170
```
    /**
     * Do the following line(s) require a deeper indentation than this line's?
     * @return True or false
     */
    default boolean requireNestedIndentation() {
        final boolean result;

        if("---".equals(this.trimmed())) {
            result = false;
        } else {
            final String trimmed = this.trimmed();
            final CharSequence prevLineLastChar = trimmed.substring(
                trimmed.length() - 1
            );
            if(prevLineLastChar.charAt(0)  == '?' && trimmed.length() == 1) {
                result = true;
            } else {
                final String otherSpecialChars = "-";
                result = otherSpecialChars.contains(prevLineLastChar);
            }


        }
        return result;
    }
```
[ ] decorators-squad--eo-yaml--trimmed
https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/YamlLine.java#L51-L82
```
    /**
     * The line's trimmed contents with comments, aliases etc removed.
     * @return Trimmed string (leading and trailing spaces) contents.
     * @todo #374:60min There's a missing condition in this method, removed
     *  as a workaround in Pull Request 375. Debug, find the reason and
     *  implement a better solution for ticket 374. This is rather low prio.
     * @checkstyle CyclomaticComplexity (100 lines)
     */
    default String trimmed() {
        String trimmed = this.value().trim();
        int i = 0;
        while(i < trimmed.length()) {
            if(i > 0 && trimmed.charAt(i) == '#') {
                if(trimmed.charAt(i - 1) == ' ') {
                    trimmed = trimmed.substring(0, i);
                    break;
                }
            } else if(trimmed.charAt(i) == '"') {
                i++;
                while(i < trimmed.length() && trimmed.charAt(i) != '"') {
                    i++;
                }
            } else if(trimmed.charAt(i) == '\'') {
                i++;
                while(i < trimmed.length() && trimmed.charAt(i) != '\'') {
                    i++;
                }
            }
            i++;
        }
        return trimmed.trim();
    }
```
[ ] devnied--Bit-lib4j--getNextByte
https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BitUtils.java#L164-L216
```
	/**
	 * Method to get The next bytes with the specified size
	 *
	 * @param pSize
	 *            the size in bit to read
	 * @param pShift
	 *            boolean to indicate if the data read will be shift to the
	 *            left.<br>
	 *            <ul>
	 *            <li>if true : (Ex 10110000b if we start read 2 bit at index 2
	 *            the returned data will be 11000000b)</li>
	 *            <li>if false : (Ex 10110000b if we start read 2 bit at index 2
	 *            the returned data will be 00110000b)</li>
	 *            </ul>
	 * @return a byte array
	 */
	public byte[] getNextByte(final int pSize, final boolean pShift) {
		byte[] tab = new byte[(int) Math.ceil(pSize / BYTE_SIZE_F)];

		if (currentBitIndex % BYTE_SIZE != 0) {
			int index = 0;
			int max = currentBitIndex + pSize;
			while (currentBitIndex < max) {
				int mod = currentBitIndex % BYTE_SIZE;
				int modTab = index % BYTE_SIZE;
				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
				if (pShift || pSize % BYTE_SIZE == 0) {
					if (mod != 0) {
						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
					} else {
						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
					}
				}
				tab[index / BYTE_SIZE] |= val;
				currentBitIndex += length;
				index += length;
			}
			if (!pShift && pSize % BYTE_SIZE != 0) {
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
[ ] devnied--Bit-lib4j--getNextLong
https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BitUtils.java#L303-L344
```
	/**
	 * This method is used to get a long with the specified size
	 *
	 * Be careful with java long bit sign. This method doesn't handle signed values.<br>
	 * For that, @see BitUtils.getNextLongSigned()
	 *
	 * @param pLength
	 *            the length of the data to read in bit
	 * @return an long
	 */
	public long getNextLong(final int pLength) {
		// allocate Size of Integer
		ByteBuffer buffer = ByteBuffer.allocate(BYTE_SIZE * 2);
		// final value
		long finalValue = 0;
		// Incremental value
		long currentValue = 0;
		// Size to read
		int readSize = pLength;
		// length max of the index
		int max = currentBitIndex + pLength;
		while (currentBitIndex < max) {
			int mod = currentBitIndex % BYTE_SIZE;
			// apply the mask to the selected byte
			currentValue = byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, readSize) & DEFAULT_VALUE;
			// Shift right the read value
			int dec = Math.max(BYTE_SIZE - (mod + readSize), 0);
			currentValue = (currentValue & DEFAULT_VALUE) >>> dec & DEFAULT_VALUE;
			// Shift left the previously read value and add the current value
			finalValue = finalValue << Math.min(readSize, BYTE_SIZE) | currentValue;
			// calculate read value size
			int val = BYTE_SIZE - mod;
			// Decrease the size left
			readSize = readSize - val;
			currentBitIndex = Math.min(currentBitIndex + val, max);
		}
		buffer.putLong(finalValue);
		// reset the current bytebuffer index to 0
		((Buffer)buffer).rewind();
		// return integer
		return buffer.getLong();
	}
```
[ ] devnied--Bit-lib4j--setNextValue
https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BitUtils.java#L577-L613
```
	/**
	 * Add Value to the current position with the specified size
	 *
	 * @param pValue
	 *            value to add
	 * @param pLength
	 *            length of the value
	 * @param pMaxSize
	 *            max size in bits
	 */
	private void setNextValue(final long pValue, final int pLength, final int pMaxSize) {
		long value = pValue;
		// Set to max value if pValue cannot be stored on pLength bits.
		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
		if (pValue > bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE - mod);
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
[ ] devnied--Bit-lib4j--toBinary
https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BytesUtils.java#L278-L297
```
	/**
	 * Convert byte array to binary String
	 *
	 * @param pBytes
	 *            byte array to convert
	 * @return a binary representation of the byte array
	 */
	public static String toBinary(final byte[] pBytes) {
		String ret = null;
		if (pBytes != null && pBytes.length > 0) {
			BigInteger val = new BigInteger(bytesToStringNoSpace(pBytes), HEXA);
			StringBuilder build = new StringBuilder(val.toString(2));
			// left pad with 0 to fit byte size
			for (int i = build.length(); i < pBytes.length * BitUtils.BYTE_SIZE; i++) {
				build.insert(0, 0);
			}
			ret = build.toString();
		}
		return ret;
	}
```
[ ] dropwizard--dropwizard-elasticsearch--fromHostAndPorts
https://github.com/dropwizard/dropwizard-elasticsearch/blob/22b4e6418177f73681a73f46d961c26bf9d290ab/./src/main/java/io/dropwizard/elasticsearch/util/TransportAddressHelper.java#L28-L47
```
    /**
     * Convert a list of {@link HostAndPort} instances to an array of {@link TransportAddress} instances.
     *
     * @param hostAndPorts a {@link List} of valid {@link HostAndPort} instances
     * @return an array of {@link TransportAddress} instances
     * @see #fromHostAndPort(com.google.common.net.HostAndPort)
     */
    public static TransportAddress[] fromHostAndPorts(final List<HostAndPort> hostAndPorts) {
        if (hostAndPorts == null) {
            return new TransportAddress[0];
        } else {
            TransportAddress[] transportAddresses = new TransportAddress[hostAndPorts.size()];

            for (int i = 0; i < hostAndPorts.size(); i++) {
                transportAddresses[i] = fromHostAndPort(hostAndPorts.get(i));
            }

            return transportAddresses;
        }
    }
```
[ ] dyn4j--dyn4j--accumulate
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/dynamics/AbstractPhysicsBody.java#L680-L720
```
	/**
	 * Accumulates the forces and torques.
	 * @param elapsedTime the elapsed time since the last call
	 * @since 3.1.0
	 */
	protected void accumulate(double elapsedTime) {
		// set the current force to zero
		this.force.zero();
		// get the number of forces
		int size = this.forces.size();
		// check if the size is greater than zero
		if (size > 0) {
			// apply all the forces
			Iterator<Force> it = this.forces.iterator();
			while(it.hasNext()) {
				Force force = it.next();
				this.force.add(force.force);
				// see if we should remove the force
				if (force.isComplete(elapsedTime)) {
					it.remove();
				}
			}
		}
		// set the current torque to zero
		this.torque = 0.0;
		// get the number of torques
		size = this.torques.size();
		// check the size
		if (size > 0) {
			// apply all the torques
			Iterator<Torque> it = this.torques.iterator();
			while(it.hasNext()) {
				Torque torque = it.next();
				this.torque += torque.torque;
				// see if we should remove the torque
				if (torque.isComplete(elapsedTime)) {
					it.remove();
				}
			}
		}
	}
```
[ ] dyn4j--dyn4j--addContactConstraint
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/world/ConstraintGraph.java#L118-L144
```
	/**
	 * Adds an interaction graph edge for the given {@link ContactConstraint}.
	 * @param contactConstraint the contact constraint
	 */
	public void addContactConstraint(ContactConstraint<T> contactConstraint) {
		T body1 = contactConstraint.getBody1();
		T body2 = contactConstraint.getBody2();
		
		ConstraintGraphNode<T> node1 = this.graph.get(body1);
		ConstraintGraphNode<T> node2 = this.graph.get(body2);
		
		// NOTE: node1/node2 shouldn't ever be null since
		// the we shouldn't generate a contact constraint
		// for bodies that don't already exist in the world
		// but it's here just in case
		if (node1 == null) {
			node1 = new ConstraintGraphNode<T>(body1);
			this.graph.put(body1, node1);
		}
		if (node2 == null) {
			node2 = new ConstraintGraphNode<T>(body2);
			this.graph.put(body2, node2);
		}
		
		node1.contactConstraints.add(contactConstraint);
		node2.contactConstraints.add(contactConstraint);
	}
```
[ ] dyn4j--dyn4j--compare
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Rotation.java#L720-L738
```
	/**
	 * Compares this {@link Rotation} with another one, based on the angle between them (The one with -&pi; &le; &theta; &le; &pi;)
	 * Returns 1 if &theta; &gt; 0, -1 if &theta; &lt; 0 and 0 otherwise
	 * @param other the {@link Rotation} to compare to
	 * @return int 
	 */
	public int compare(Rotation other) {
		// cmp = sin(&thetasym;) where &thetasym; is the angle between this rotation and the other
		// So we can decide what to return based on the sign of cmp
		double cmp = this.cross(other);
		
		if (cmp > 0.0) {
			return 1;
		} else if (cmp < 0.0) {
			return -1;
		} else {
			return 0;
		}
	}
```
[ ] dyn4j--dyn4j--distance
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/narrowphase/CircleDetector.java#L117-L158
```
	/**
	 * Fast method for determining the distance between two {@link Circle}s.
	 * <p>
	 * Returns true if the given {@link Circle}s are separated and places the
	 * separating vector and distance in the given {@link Separation} object.
	 * <p>
	 * NOTE: It's the responsibility of the caller to clear the given {@link Separation} object
	 * before calling this method.
	 * @param circle1 the first {@link Circle}
	 * @param transform1 the first {@link Circle}'s {@link Transform}
	 * @param circle2 the second {@link Circle}
	 * @param transform2 the second {@link Circle}'s {@link Transform}
	 * @param separation the {@link Separation} object to fill
	 * @return boolean
	 */
	public static final boolean distance(Circle circle1, Transform transform1, Circle circle2, Transform transform2, Separation separation) {
		// get their world centers
		Vector2 ce1 = transform1.getTransformed(circle1.getCenter());
		Vector2 ce2 = transform2.getTransformed(circle2.getCenter());
		// get the radii
		double r1 = circle1.getRadius();
		double r2 = circle2.getRadius();
		// create a vector from one center to the other
		Vector2 v = ce1.to(ce2);
		// check the magnitude against the sum of the radii
		double radii = r1 + r2;
		// get the magnitude squared
		double mag = v.getMagnitudeSquared();
		// check difference
		if (mag >= radii * radii) {
			// then the circles are separated
			separation.distance = v.normalize() - radii;
			separation.normal.x = v.x;
			separation.normal.y = v.y;
			separation.point1.x = ce1.x + v.x * r1;
			separation.point1.y = ce1.y + v.y * r1;
			separation.point2.x = ce2.x - v.x * r2;
			separation.point2.y = ce2.y - v.y * r2;
			return true;
		}
		return false;
	}
```
[ ] dyn4j--dyn4j--equals-6
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Vector2.java#L287-L309
```
    /**
     * Returns true if the given vector and this {@link Vector2}
	 * are the same within a given tolerance.
	 * @param vector the vector to compare to
	 * @param epsilon the tolerance in the range [0, &infin;)
	 * @return boolean
	 * @since 5.0.2
     */
    public boolean equals(Vector2 vector, double epsilon) {
        if (vector == null) {
            return false;
        }
        if (vector == this) {
        	return true;
        }
        if (Math.abs(vector.x - this.x) > epsilon) {
        	return false;
        }
        if (Math.abs(vector.y - this.y) > epsilon) {
        	return false;
        }
        return true;
    }
```
[ ] dyn4j--dyn4j--equals-9
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Vector3.java#L246-L256
```
	/**
	 * Returns true if the x, y and z components of this {@link Vector3}
	 * are the same as the given x, y and z components.
	 * @param x the x coordinate of the {@link Vector3} to compare to
	 * @param y the y coordinate of the {@link Vector3} to compare to
	 * @param z the z coordinate of the {@link Vector3} to compare to
	 * @return boolean
	 */
	public boolean equals(double x, double y, double z) {
		return this.x == x && this.y == y && this.z == z;
	}
```
[ ] dyn4j--dyn4j--findNext-4
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/broadphase/DynamicAABBTree.java#L955-L985
```
		/**
		 * Returns true if there's another pair to process and sets
		 * the nextPair field to that pair.
		 * @return boolean
		 */
		private boolean findNext() {
			// iterate through the list of AABBs to test the entire
			// broadphase against
			while (this.iterator.hasNext() || this.currentLeaf != null) {
				// if the current AABB is null, then grab a new one
				if (this.currentLeaf == null) {
					this.currentLeaf = this.iterator.next();
				}
				
				// if the current node in the broadphase is null
				// then we need to start at the root
				if (this.currentNode == null) {
					// start at the root node
					this.currentNode = DynamicAABBTree.this.root;
				}
			
				// is there another collision with the current leaf?
				if (this.findNextForCurrentLeaf()) {
					return true;
				}
				
				// if not we need to move to the next leaf
			}
			
			return false;
		}
```
[ ] dyn4j--dyn4j--findNextForCurrentLeaf
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/broadphase/DynamicAABBTree.java#L987-L1085
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
[ ] dyn4j--dyn4j--fromDiff
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/AdaptiveDecimal.java#L550-L601
```
	/**
	 * Given two unrolled expansions (a0, a1) and (b0, b1) performs the difference
	 * (a0, a1) - (b0, b1) and stores the 4 component result in the given {@link AdaptiveDecimal} {@code result}.
	 * In the same way as with {@link AdaptiveDecimal#sum(AdaptiveDecimal, AdaptiveDecimal)} if {@code result} is null
	 * a new one is allocated, otherwise the existing is cleared and used.
	 * Does not perform zero elimination.
	 * This is also a helper method to allow fast computation of the cross product
	 * without the overhead of creating new {@link AdaptiveDecimal} and performing
	 * the generalized sum procedure.
	 * 
	 * @param a0 The first component of a
	 * @param a1 The second component of a
	 * @param b0 The first component of b
	 * @param b1 The second component of b
	 * @param result The {@link AdaptiveDecimal} in which the difference is stored or null to allocate a new one
	 * @return The result
	 */
	static AdaptiveDecimal fromDiff(double a0, double a1, double b0, double b1, AdaptiveDecimal result) {
		// the exact order of those operations is necessary for correct functionality 
		// This is a rewrite of the corresponding Two_Two_Diff macro in the original code
		
		// allocate a new instance of sufficient size if result is null or just clear
		if (result == null) {
			result = new AdaptiveDecimal(4);
		} else {
			result.clear();	
		}
		
		// x0-x1-x2-x3 store the resulting components with increasing magnitude
		double x0, x1, x2, x3;
		
		// variable to store immediate results for each pair of Diff/Sum
		double imm;
		
		// variables to store immediate results across the two pairs 
		double imm1, imm2;
		
		// Diff (a0, a1) - b0, result = (x0, imm1, imm2)
		x0 = AdaptiveDecimal.getErrorComponentFromDifference(a0, b0, imm = a0 - b0);
		imm1 = AdaptiveDecimal.getErrorComponentFromSum(a1, imm, imm2 = a1 + imm);
		
		// Diff (imm1, imm2) - b1, result = (x1, x2, x3)
		x1 = AdaptiveDecimal.getErrorComponentFromDifference(imm1, b1, imm = imm1 - b1);
		x2 = AdaptiveDecimal.getErrorComponentFromSum(imm2, imm, x3 = imm2 + imm);
		
		result.append(x0);
		result.append(x1);
		result.append(x2);
		result.append(x3);
		
		return result;
	}
```
[ ] dyn4j--dyn4j--getErrorComponentFromProduct
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/AdaptiveDecimal.java#L656-L686
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
[ ] dyn4j--dyn4j--getFarthestPointOnBoundedEllipse
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Ellipse.java#L435-L496
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
			if (fx2 < fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
			}
		}
			
		return p;
	}
```
[ ] dyn4j--dyn4j--getFarthestVertexFromLine
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/DouglasPeucker.java#L235-L275
```
	/**
	 * Returns the farthest vertex in the polyline from the line created by lineVertex1 and lineVertex2.
	 * <p>
	 * O(n)
	 * @param lineVertex1 the first vertex of the line
	 * @param lineVertex2 the second vertex of the line
	 * @param polyline the entire polyline
	 * @return {@link FarthestVertex}
	 */
	private final FarthestVertex getFarthestVertexFromLine(SimplePolygonVertex lineVertex1, SimplePolygonVertex lineVertex2, List<SimplePolygonVertex> polyline) {
		int index = -1;
		double distance = 0.0;
		
		Vector2 lp1 = lineVertex1.point;
		Vector2 lp2 = lineVertex2.point;
		
		// find the vertex on the polyline that's farthest from the line created
		// by lineVertex1 and lineVertex2
		int size = polyline.size();
		Vector2 line = lp1.to(lp2);
		Vector2 lineNormal = line.getLeftHandOrthogonalVector();
		lineNormal.normalize();
		for (int i = 0; i < size; i++) {
			Vector2 vert = polyline.get(i).point;
			double test = Math.abs(lp1.to(vert).dot(lineNormal));
			if (test > distance) {
				distance = test;
				index = i;
			}
		}
		
		// make sure we found a winner
		if (index < 0) {
			// then they were all colinear, so take the middle one
			// NOTE: integer division here
			index = size / 2;
			distance = 0.0;
		}
		
		return new FarthestVertex(index, distance);
	}
```
[ ] dyn4j--dyn4j--getLineIntersection
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Segment.java#L344-L395
```
	/**
	 * Returns the intersection point of the two lines or null if they are parallel or coincident.
	 * <p>
	 * If we let:
	 * <p style="white-space: pre;"> A = A<sub>p2</sub> - A<sub>p1</sub>
	 * B = B<sub>p2</sub> - B<sub>p1</sub></p>
	 * we can create two parametric equations:
	 * <p style="white-space: pre;"> Q = A<sub>p1</sub> + t<sub>a</sub>A
	 * Q = B<sub>p1</sub> + t<sub>b</sub>B</p>
	 * Where Q is the intersection point:
	 * <p style="white-space: pre;"> A<sub>p1</sub> + t<sub>a</sub>A = B<sub>p1</sub> + t<sub>b</sub>B</p>
	 * We can solve for t<sub>b</sub> by applying the cross product with A on both sides:
	 * <p style="white-space: pre;"> (A<sub>p1</sub> + t<sub>a</sub>A) x A = (B<sub>p1</sub> + t<sub>b</sub>B) x A
	 * A<sub>p1</sub> x A = B<sub>p1</sub> x A + t<sub>b</sub>B x A
	 * (A<sub>p1</sub> - B<sub>p1</sub>) x A = t<sub>b</sub>B x A
	 * t<sub>b</sub> = ((A<sub>p1</sub> - B<sub>p1</sub>) x A) / (B x A)</p>
	 * If B x A == 0 then the lines are parallel.  If both the top and bottom are zero 
	 * then the lines are coincident.
	 * <p>
	 * If the lines are parallel or coincident, null is returned.
	 * @param ap1 the first point of the first line
	 * @param ap2 the second point of the first line
	 * @param bp1 the first point of the second line
	 * @param bp2 the second point of the second line
	 * @return Vector2 the intersection point; null if the lines are parallel or coincident
	 * @see #getSegmentIntersection(Vector2, Vector2, Vector2, Vector2)
	 * @throws NullPointerException if ap1, ap2, bp1 or bp2 is null
	 * @since 3.1.1
	 */
	public static final Vector2 getLineIntersection(Vector2 ap1, Vector2 ap2, Vector2 bp1, Vector2 bp2) {
		Vector2 A = ap1.to(ap2);
		Vector2 B = bp1.to(bp2);
		
		// compute the bottom
		double BxA = B.cross(A);
		if (Math.abs(BxA) <= Epsilon.E) {
			// the lines are parallel and don't intersect
			return null;
		}
		
		// compute the top
		double ambxA = ap1.difference(bp1).cross(A);
		if (Math.abs(ambxA) <= Epsilon.E) {
			// the lines are coincident
			return null;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		// compute the intersection point
		return B.product(tb).add(bp1);
	}
```
[ ] dyn4j--dyn4j--getMass
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Mass.java#L351-L364
```
	/**
	 * Returns the mass.
	 * <p>
	 * NOTE: if this mass is type {@link MassType#INFINITE} or {@link MassType#FIXED_LINEAR_VELOCITY}
	 * this method returns zero.
	 * @return double
	 */
	public double getMass() {
		if (this.type == MassType.INFINITE || this.type == MassType.FIXED_LINEAR_VELOCITY) {
			return 0.0;
		} else {
			return this.mass;
		}
	}
```
[ ] dyn4j--dyn4j--getReducedMass
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/dynamics/joint/AbstractPairedBodyJoint.java#L153-L175
```
	/**
	 * Returns the reduced mass of this pair of bodies.
	 * <p>
	 * The reduced mass is used to solve spring/damper problems as a single body rather
	 * than as a system of two bodies.
	 * <p>
	 * <a href="https://en.wikipedia.org/wiki/Reduced_mass">https://en.wikipedia.org/wiki/Reduced_mass</a>
	 * @return double
	 */
	protected final double getReducedMass() {
		// https://en.wikipedia.org/wiki/Reduced_mass
		double m1 = this.body1.getMass().getMass();
		double m2 = this.body2.getMass().getMass();
		
		// compute the mass
		if (m1 > 0.0 && m2 > 0.0) {
			return m1 * m2 / (m1 + m2);
		} else if (m1 > 0.0) {
			return m1;
		} else {
			return m2;
		}
	}
```
[ ] dyn4j--dyn4j--getSquaredDistance
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Ellipse.java#L498-L534
```
	/**
	 * Returns the distance from the ellipse at the given x to the given point q.
	 * @param a2 the ellipse semi-major axis squared (a * a)
	 * @param ba the ellipse semi-minor axis divided by the semi-major axis (b / a)
	 * @param x the x of the point on the ellipse
	 * @param q the query point
	 * @param p output; the point on the ellipse
	 * @return double
	 * @since 3.4.0
	 */
	private static double getSquaredDistance(double a2, double ba, double x, Vector2 q, Vector2 p) {
		// compute the y value for the given x on the ellipse:
		// (x^2/a^2) + (y^2/b^2) = 1
		// y^2 = (1 - (x / a)^2) * b^2
		// y^2 = b^2/a^2(a^2 - x^2)
		// y = (b / a) * sqrt(a^2 - x^2)
		double a2x2 = a2 - (x * x);
		if (a2x2 < 0) {
			// this should never happen, but just in case of numeric instability
			// we'll just set it to zero
			a2x2 = 0;
			// x^2/a^2 can never be greater than 1 since a must always be
			// greater than or equal to the largest x value on the ellipse
		}
		double sa2x2 = Math.sqrt(a2x2);
		double y = ba * sa2x2;
		
		// compute the distance from the ellipse point to the query point
		double xx = (q.x - x);
		double yy = (q.y - y);
		double d2 = xx * xx + yy * yy;
		p.x = x;
		p.y = y;
		
		// return the distance
		return d2;
	}
```
[ ] dyn4j--dyn4j--hertelMehlhorn
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/DoubleEdgeList.java#L685-L743
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().origin;
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.getPrevious().origin;
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
[ ] dyn4j--dyn4j--initialize
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/DoubleEdgeList.java#L80-L159
```
	/**
	 * Initializes the DCEL class given the points of the polygon.
	 * @param points the points of the polygon
	 */
	public void initialize(Vector2[] points) {
		// get the number of points
		int size = points.length;
		
		// we will always have exactly one face at the beginning
		DoubleEdgeListFace face = new DoubleEdgeListFace();
		this.faces.add(face);
		
		DoubleEdgeListHalfEdge prevLeftEdge = null;
		DoubleEdgeListHalfEdge prevRightEdge = null;
		
		// loop over the points creating the vertices and
		// half edges for the data structure
		for (int i = 0; i < size; i++) {
			Vector2 point = points[i];
			
			DoubleEdgeListVertex vertex = new DoubleEdgeListVertex(point);
			DoubleEdgeListHalfEdge left = new DoubleEdgeListHalfEdge();
			DoubleEdgeListHalfEdge right = new DoubleEdgeListHalfEdge();
			
			// create and populate the left
			// and right half edges
			left.face = face;
			left.next = null;
			left.origin = vertex;
			left.twin = right;
			
			right.face = null;
			right.next = prevRightEdge;
			right.origin = null;
			right.twin = left;
			
			// add the edges the edge list
			this.edges.add(left);
			this.edges.add(right);
			
			// populate the vertex
			vertex.leaving = left;
			
			// add the vertex to the vertices list
			this.vertices.add(vertex);
			
			// set the previous next edge to this left edge
			if (prevLeftEdge != null) {
				prevLeftEdge.next = left;
			}
			
			// set the previous right edge origin to this vertex
			if (prevRightEdge != null) {
				prevRightEdge.origin = vertex;
			}
			
			// set the new previous edges
			prevLeftEdge = left;
			prevRightEdge = right;
		}
		
		// set the last left edge's next pointer to the
		// first left edge we created
		DoubleEdgeListHalfEdge firstLeftEdge = this.edges.get(0);
		prevLeftEdge.next = firstLeftEdge;
		
		// set the first right edge's next pointer
		// to the last right edge we created
		// (note that right edges are at odd indices)
		DoubleEdgeListHalfEdge firstRightEdge = this.edges.get(1);
		firstRightEdge.next = prevRightEdge;
		// set the last right edge's origin to the first
		// vertex in the list
		prevRightEdge.origin = this.vertices.get(0);
		
		// set the edge of the only face to the first
		// left edge
		// (note that the interior of each face has CCW winding)
		face.edge = firstLeftEdge;
	}
```
[ ] dyn4j--dyn4j--intersection
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/AABB.java#L406-L433
```
	/**
	 * Performs the intersection of this {@link AABB} and the given {@link AABB} placing
	 * the result into this {@link AABB} and then returns this {@link AABB}.
	 * <p>
	 * If the given {@link AABB} does not overlap this {@link AABB}, this {@link AABB} is
	 * set to a zero {@link AABB}.
	 * @param aabb the {@link AABB} to intersect
	 * @return {@link AABB}
	 * @since 3.1.1
	 */
	public AABB intersection(AABB aabb) {
		this.minX = Math.max(this.minX, aabb.minX);
		this.minY = Math.max(this.minY, aabb.minY);
		this.maxX = Math.min(this.maxX, aabb.maxX);
		this.maxY = Math.min(this.maxY, aabb.maxY);
		
		// check for a bad AABB
		if (this.minX > this.maxX || this.minY > this.maxY) {
			// the two AABBs were not overlapping
			// set this AABB to a degenerate one
			this.minX = 0.0;
			this.minY = 0.0;
			this.maxX = 0.0;
			this.maxY = 0.0;
		}
		
		return this;
	}
```
[ ] dyn4j--dyn4j--intersects
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/AbstractSimplifier.java#L165-L232
```
	/**
	 * Returns true if the given segments intersect each other.
	 * @param a1 the first point of the first segment
	 * @param a2 the second point of the first segment
	 * @param b1 the first point of the second segment
	 * @param b2 the second point of the second segment
	 * @return boolean
	 */
	protected final boolean intersects(Vector2 a1, Vector2 a2, Vector2 b1, Vector2 b2) {
		Vector2 A = a1.to(a2);
		Vector2 B = b1.to(b2);

		// compute the bottom
		double BxA = B.cross(A);
		// compute the top
		double ambxA = a1.difference(b1).cross(A);
		
		// if the bottom is zero, then the segments are either parallel or coincident
		if (Math.abs(BxA) <= Epsilon.E) {
			// if the top is zero, then the segments are coincident
			if (Math.abs(ambxA) <= Epsilon.E) {
				// project the segment points onto the segment vector (which
				// is the same for A and B since they are coincident)
				A.normalize();
				double ad1 = a1.dot(A);
				double ad2 = a2.dot(A);
				double bd1 = b1.dot(A);
				double bd2 = b2.dot(A);
				
				// then compare their location on the number line for intersection
				Interval ia = new Interval(ad1, ad2);
				Interval ib = new Interval(bd1 < bd2 ? bd1 : bd2, bd1 > bd2 ? bd1 : bd2);
				
				if (ia.overlaps(ib)) {
					return true;
				}
			}
			
			// otherwise they are parallel
			return false;
		}
		
		// if just the top is zero, then there's no intersection
		if (Math.abs(ambxA) <= Epsilon.E) {
			return false;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		if (tb <= 0.0 || tb >= 1.0) {
			// no intersection
			return false;
		}
		
		// compute the intersection point
		Vector2 ip = B.product(tb).add(b1);
		
		// since both are segments we need to verify that
		// ta is also valid.
		// compute ta
		double ta = ip.difference(a1).dot(A) / A.dot(A);
		if (ta <= 0.0 || ta >= 1.0) {
			// no intersection
			return false;
		}
		
		return true;
	}
```
[ ] dyn4j--dyn4j--isAllowed-2
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/TypeFilter.java#L88-L121
```
	/**
	 * Returns true under the following conditions:
	 * <ol>
	 * <li>If this filter is the same type as the given filter.</li>
	 * <li>If this filter type is a descendant of the given filter's type.</li>
	 * <li>If the given filter's type is a descendant of this filter's type.</li>
	 * </ol>
	 * If the given filter is not of type {@link TypeFilter} then false is returned.
	 * <p>
	 * If the given filter is null then false is returned.
	 * @param filter the other filter
	 */
	@Override
	public boolean isAllowed(Filter filter) {
		// if its null then just return
		if (filter == null) return false;
		// check for the same instance
		if (this == filter) return true;
		// make sure the given filter is a TypeFilter
		if (filter instanceof TypeFilter) {
			// because the TypeFilter class is abstract, this.getClass() should never return
			// TypeFilter, but should return the type of the class that extends TypeFilter
			
			// then check the types
			if (this.getClass().isInstance(filter) || filter.getClass().isInstance(this)) {
				// if they are the same type then return true
				// if the given filter is a descendant type of this filter type then return true
				// if this type is a descendant of the given filter's type then return true
				return true;
			}
		}
		// otherwise return false
		return false;
	}
```
[ ] dyn4j--dyn4j--isFallbackRequired
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/narrowphase/FallbackNarrowphaseDetector.java#L149-L165
```
	/**
	 * Returns true if the fallback {@link NarrowphaseDetector} should be used rather
	 * than the primary.
	 * @param convex1 the first convex
	 * @param convex2 the second convex
	 * @return boolean
	 */
	public boolean isFallbackRequired(Convex convex1, Convex convex2) {
		int size = this.fallbackConditions.size();
		for (int i = 0; i < size; i++) {
			FallbackCondition condition = this.fallbackConditions.get(i);
			if (condition != null && condition.isMatch(convex1, convex2)) {
				return true;
			}
		}
		return false;
	}
```
[ ] dyn4j--dyn4j--isVisible
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/Bayazit.java#L404-L449
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
[ ] dyn4j--dyn4j--merge-2
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/hull/LinkedVertexHull.java#L90-L189
```
	/**
	 * Merges the two given convex {@link LinkedVertexHull}s into one convex {@link LinkedVertexHull}.
	 * <p>
	 * The left {@link LinkedVertexHull} should contain only points whose x coordinates are
	 * less than all the points in the right {@link LinkedVertexHull}.
	 * @param left the left convex {@link LinkedVertexHull}
	 * @param right the right convex {@link LinkedVertexHull}
	 * @return {@link LinkedVertexHull} the merged convex hull
	 */
	public static final LinkedVertexHull merge(LinkedVertexHull left, LinkedVertexHull right) {
		// This merge algorithm handles all cases, including point-point and point-segment without special cases.
		// It finds the upper and lower edges that connect the two hulls such that the resulting hull remains convex
		
		LinkedVertexHull hull = new LinkedVertexHull();
		hull.leftMost = left.leftMost;
		hull.rightMost = right.rightMost;
		
		LinkedVertex lu = left.rightMost;
		LinkedVertex ru = right.leftMost;
		
		// We don't use strict inequalities when checking the result of getLocation
		// so we can remove coincident points in the hull.
		// As a result we must limit the number of loops that go to the left or right
		// because else ru = ru.prev can loop over and never terminate
		// We can walk at most side.size - 1 before looping over
		int limitRightU = right.size - 1;
		int limitLeftU = left.size - 1;
		
		while (true) {
			LinkedVertex prevLu = lu;
			LinkedVertex prevRu = ru;
			
			while (limitRightU > 0 && RobustGeometry.getLocation(ru.next.point, lu.point, ru.point) <= 0) {
				ru = ru.next;
				limitRightU--;
			}
			
			while (limitLeftU > 0 && RobustGeometry.getLocation(lu.prev.point, lu.point, ru.point) <= 0) {
				lu = lu.prev;
				limitLeftU--;
			}
			
			// If no progress is made there's nothing else to do
			if (lu == prevLu && ru == prevRu) {
				break;
			}
		}
		
		// Same as before, for the other side
		
		LinkedVertex ll = left.rightMost;
		LinkedVertex rl = right.leftMost;
		
		int limitRightL = right.size - 1;
		int limitLeftL = left.size - 1;
		
		while (true) {
			LinkedVertex prevLl = ll;
			LinkedVertex prevRl = rl;
			
			while (limitRightL > 0 && RobustGeometry.getLocation(rl.prev.point, ll.point, rl.point) >= 0) {
				rl = rl.prev;
				limitRightL--;
			}
			
			while (limitLeftL > 0 && RobustGeometry.getLocation(ll.next.point, ll.point, rl.point) >= 0) {
				ll = ll.next;
				limitLeftL--;
			}
			
			// If no progress is made there's nothing else to do
			if (ll == prevLl && rl == prevRl) {
				break;
			}
		}
		
		// link the hull
		lu.next = ru;
		ru.prev = lu;
		
		ll.prev = rl;
		rl.next = ll;
		
		// We could compute size with a closed-form type based on the four values
		// of limitLeft/Right/L/U but it is not straightforward and there is no observable
		// speed gain. So use a simple loop instead
		int size = 0;
		LinkedVertex v = lu;
		
		do {
			size ++;
			v = v.next;
		} while (v != lu);
		
		// set the size
		hull.size = size;
		
		// return the merged hull
		return hull;
	}
```
[ ] dyn4j--dyn4j--overlaps
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/AABB.java#L531-L541
```
	/**
	 * Returns true if the given {@link AABB} and this {@link AABB} overlap.
	 * @param aabb the {@link AABB} to test
	 * @return boolean true if the {@link AABB}s overlap
	 */
	public boolean overlaps(AABB aabb) {
		return this.minX <= aabb.maxX &&
				this.maxX >= aabb.minX &&
				this.minY <= aabb.maxY &&
				this.maxY >= aabb.minY;
	}
```
[ ] dyn4j--dyn4j--process
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/narrowphase/LinkPostProcessor.java#L60-L154
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
[ ] dyn4j--dyn4j--pushLeftFrom
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/BinarySearchTreeIterator.java#L118-L140
```
	/**
	 * Pushes the required nodes onto the stack to begin iterating
	 * nodes in order starting from the given value.
	 * @param from the value to start iterating from
	 * @since 3.2.3
	 */
	protected void pushLeftFrom(E from) {
		BinarySearchTreeNode<E> node = this.root;
		while (node != null) {
			int cmp = from.compareTo(node.comparable);
			if (cmp < 0) {
				// go left
				this.stack.push(node);
				node = node.left;
			} else if (cmp > 0) {
				// go right
				node = node.right;
			} else {
				this.stack.push(node);
				break;
			}
		}
	}
```
[ ] dyn4j--dyn4j--raycast
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/broadphase/AbstractBroadphaseDetector.java#L183-L217
```
	/**
	 * Returns true if the ray and AABB intersect.
	 * <p>
	 * This method is ideally called for a number of AABBs where the invDx and invDy can
	 * be computed once.
	 * <p>
	 * <a href="http://tavianator.com/2011/05/fast-branchless-raybounding-box-intersections/">http://tavianator.com/2011/05/fast-branchless-raybounding-box-intersections/</a>
	 * @param start the start position of the ray
	 * @param length the length of the ray
	 * @param invDx the inverse of the x component of the ray direction
	 * @param invDy the inverse of the y component of the ray direction
	 * @param aabb the AABB to test
	 * @return true if the AABB and ray intersect
	 */
	static boolean raycast(Vector2 start, double length, double invDx, double invDy, AABB aabb) {
		// see here for implementation details
		// http://tavianator.com/2011/05/fast-branchless-raybounding-box-intersections/
		double tx1 = (aabb.getMinX() - start.x) * invDx;
		double tx2 = (aabb.getMaxX() - start.x) * invDx;

		double tmin = Math.min(tx1, tx2);
		double tmax = Math.max(tx1, tx2);

		double ty1 = (aabb.getMinY() - start.y) * invDy;
		double ty2 = (aabb.getMaxY() - start.y) * invDy;

		tmin = Math.max(tmin, Math.min(ty1, ty2));
		tmax = Math.min(tmax, Math.max(ty1, ty2));
		// the ray is pointing in the opposite direction
		if (tmax < 0) return false;
		// consider the ray length
		if (tmin > length) return false;
		// along the ray, tmax should be larger than tmin
		return tmax >= tmin;
	}
```
[ ] dyn4j--dyn4j--remove-3
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/SegmentTree.java#L202-L262
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (this.root == null) return;
		// check the root node
		if (node == this.root) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.left == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(left.aabb, right.aabb);
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
[ ] dyn4j--dyn4j--removeVertex-2
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/Visvalingam.java#L210-L263
```
	/**
	 * Removes the given vertex from the queue and segment tree.
	 * @param v the vertex to remove
	 * @param queue the queue to remove the vertex from
	 * @param tree the segment tree to remove the vertex from
	 */
	private final boolean removeVertex(AreaTrackedVertex v, Queue<AreaTrackedVertex> queue, SegmentTree tree) {
		Vector2 v0 = null;
		Vector2 v1 = null;
		Vector2 v2 = null;
		
		AreaTrackedVertex tprev = (AreaTrackedVertex)v.prev;
		AreaTrackedVertex tnext = (AreaTrackedVertex)v.next;
		SegmentTreeLeaf tprevSegment = v.prevSegment;
		SegmentTreeLeaf tnextSegment = v.nextSegment;
		
		tprev.next = tnext;
		tnext.prev = tprev;
		
		// recompute the previous segment's triangular area
		v0 = tprev.prev.point;
		v1 = tprev.point;
		v2 = tnext.point;
		tprev.area = getTriangleArea(v0, v1, v2);

		// recompute the next segment's triangular area
		v0 = tprev.point;
		v1 = tnext.point;
		v2 = tnext.next.point;
		tnext.area = getTriangleArea(v0, v1, v2);
		
		// build a new segment with the given vertex removed
		v1 = tprev.point;
		v2 = tnext.point;
		
		// update the segment tree to account for the removed segments/vertex
		tprev.nextSegment = new SegmentTreeLeaf(v1, v2, tprev.index, tnext.index);
		tnext.prevSegment = tprev.nextSegment;
		// remove the two segments attached to the removed vertex
		tree.remove(tprevSegment);
		tree.remove(tnextSegment);
		// add the new segment to the segment tree
		tree.add(tprev.nextSegment);
		
		// remove the adjacent vertices from the queue
		queue.remove(tprev);
		queue.remove(tnext);
		
		// add them back to the queue so they are sorted in the correct place
		queue.add(tprev);
		queue.add(tnext);
		
		return tprev == tnext;
	}
```
[ ] dyn4j--dyn4j--setFromPoints
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/AABB.java#L97-L124
```
	/**
	 * Method to create the valid AABB defined by the two points A(point1x, point1y) and B(point2x, point2y) and places
	 * the result in the given AABB.
	 * @param point1x The x coordinate of point A
	 * @param point1y The y coordinate of point A
	 * @param point2x The x coordinate of point B
	 * @param point2y The y coordinate of point B
	 * @param result the AABB to set
	 * @since 4.1.0
	 */
	public static void setFromPoints(double point1x, double point1y, double point2x, double point2y, AABB result) {
		if (point2x < point1x) {
			double temp = point1x;
			point1x = point2x;
			point2x = temp;
		}
		
		if (point2y < point1y) {
			double temp = point1y;
			point1y = point2y;
			point2y = temp;
		}
		
		result.minX = point1x;
		result.minY = point1y;
		result.maxX = point2x;
		result.maxY = point2y;
	}
```
[ ] dyn4j--dyn4j--solve33
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Matrix33.java#L508-L545
```
	/**
	 * Solves the system of linear equations:
	 * <p style="white-space: pre;"> Ax = b
	 * Multiply by A<sup>-1</sup> on both sides
	 * x = A<sup>-1</sup>b</p>
	 * @param b the b {@link Vector3}
	 * @return {@link Vector3} the x vector
	 */
	public Vector3 solve33(Vector3 b) {
		// get the determinant
		double det = this.determinant();
		// check for zero determinant
		if (Math.abs(det) > Epsilon.E) {
			det = 1.0 / det;
		} else {
			det = 0.0;
		}
		
		Vector3 r = new Vector3();
		
		double m00 =  this.m11 * this.m22 - this.m12 * this.m21;
		double m01 = -this.m01 * this.m22 + this.m21 * this.m02;
		double m02 =  this.m01 * this.m12 - this.m11 * this.m02;
		
		double m10 = -this.m10 * this.m22 + this.m20 * this.m12;
		double m11 =  this.m00 * this.m22 - this.m20 * this.m02;
		double m12 = -this.m00 * this.m12 + this.m10 * this.m02;
		
		double m20 =  this.m10 * this.m21 - this.m20 * this.m11;
		double m21 = -this.m00 * this.m21 + this.m20 * this.m01;
		double m22 =  this.m00 * this.m11 - this.m10 * this.m01;
		
		r.x = det * (m00 * b.x + m01 * b.y + m02 * b.z);
		r.y = det * (m10 * b.x + m11 * b.y + m12 * b.z);
		r.z = det * (m20 * b.x + m21 * b.y + m22 * b.z);
		
		return r;
	}
```
[ ] dyn4j--dyn4j--triangulateYMonotonePolygon
https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/DoubleEdgeList.java#L464-L561
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
[ ] dynaconf--dynaconf--__init__-3
https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/utils/parse_conf.py#L158-L196
```
    def __init__(self, value, box_settings):
        """
        normally value will be a string like
        `0 foo` or `-1 foo` and needs to get split
        but value can also be just a single string with or without space
        like `foo` and in this case it will be treated as `0 foo`
        but it can also be `foo bar` and in this case it will be treated as `0 foo bar`
        we need to check if the first part is a number
        if it is not a number then we will treat it as `0 value`
        if it is a number then we will split it as `index, value`
        this must use a regex to match value, examples:
            -1 foo -> index = -1, value = foo
            0 foo -> index = 0, value = foo
            0 foo bar -> index = 0, value = foo bar
            0 42 -> index = 0, value = 42
            0 42 foo -> index = 0, value = 42 foo
            foo -> index = 0, value = foo
            foo bar -> index = 0, value = foo bar
            42 -> index = 0, value = 42
            42 foo -> index = 42, value = foo
            42 foo bar -> index = 42, value = foo bar
        """
        self.box_settings = box_settings

        try:
            if value.lstrip("-+")[0].isdigit():
                # `0 foo` or `-1 foo` or `42 foo` or `42`(raise ValueError)
                index, value = value.split(" ", 1)
            else:
                # `foo` or `foo bar`
                index, value = 0, value
        except ValueError:
            # `42` or any other non split able value
            index, value = 0, value

        self.index = int(index)
        self.value = parse_conf_data(
            value, tomlfy=True, box_settings=box_settings
        )
```
[ ] dynaconf--dynaconf--_ensure_serializable
https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/utils/inspect.py#L303-L320
```
def _ensure_serializable(data: DataList | DataDict) -> dict | list:
    """
    Converts box dict or list types to regular python dict or list
    Bypasses other values.
    {
        "foo": [1,2,3, {"a": "A", "b": "B"}],
        "bar": {"a": "A", "b": [1,2,3]},
    }
    """
    if isinstance(data, (DataList, list)):
        return [_ensure_serializable(v) for v in data]
    elif isinstance(data, (DataDict, dict)):
        return {
            k: _ensure_serializable(v)
            for k, v in data.items()  # type: ignore
        }
    else:
        return data if isinstance(data, (int, bool, float)) else str(data)
```
[ ] dynaconf--dynaconf--_get_unique_hook_id
https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/loaders/__init__.py#L150-L163
```
def _get_unique_hook_id(hook_func, hook_source):
    """get unique identifier for a hook function.
    in most of cases this will be the function name@source_file
    however, if the function is a lambda, it will be a hash of the code object.
    because lambda functions are not hashable itself and we can't rely on its id.
    """
    hook_unique_id = hook_func.__name__
    if hook_unique_id == "<lambda>":
        frame_info = getattr(hook_func, "__code__", None)
        if frame_info:
            hook_unique_id = f"lambda_{hash(frame_info.co_code)}"
        else:
            hook_unique_id = f"lambda_{id(hook_func)}"
    return f"{hook_unique_id}@{hook_source}"
```
[ ] dynaconf--dynaconf--as_dict
https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/base.py#L346-L359
```
    def as_dict(self, env=None, internal=False):
        """Returns a dictionary with set key and values.

        :param env: Str env name, default self.current_env `DEVELOPMENT`
        :param internal: bool - should include dynaconf internal vars?
        """
        ctx_mgr = suppress() if env is None else self.using_env(env)
        with ctx_mgr:
            data = self.store.to_dict().copy()
            # if not internal remove internal settings
            if not internal:
                for name in UPPER_DEFAULT_SETTINGS:
                    data.pop(name, None)
            return data
```
[ ] dynaconf--dynaconf--get_hooks
https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/hooking.py#L149-L162
```
def get_hooks(obj):
    """get registered hooks from object
    must try different casing and accessors because of
    tests and casing mode set on dynaconf.
    """
    attr = "_registered_hooks"
    for key in [attr, attr.upper()]:
        if hasattr(obj, key):
            return getattr(obj, key)
        elif isinstance(obj, dict) and key in obj:
            return obj[key]
        elif hasattr(obj, "_store") and key in obj._store:
            return obj._store[key]
    return {}
```
[ ] dynaconf--dynaconf--recursive_get
https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/utils/__init__.py#L146-L165
```
def recursive_get(
    obj: DataDict | dict[str, int] | dict[str, str | int],
    names: list[str] | None,
) -> Any:
    """Given a dot accessible object and a list of names `foo.bar.[1].zaz`
    gets recursively all names one by one obj.foo.bar.[1].zaz.
    """
    if not names or obj is None:
        return
    head, *tail = names
    if "[" not in head:
        result = getattr(obj, head, None)
    else:
        index = int(head.replace("[", "").replace("]", ""))
        result = obj[index] if index < len(obj) else []

    if not tail:
        return result

    return recursive_get(result, tail)
```
[ ] dynaconf--dynaconf--to_dict
https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/nodes.py#L170-L187
```
    def to_dict(self):
        """
        Turn the DataDict and sub DataDicts back into a native python dictionary.

        :return: python dictionary of this DataDict
        """
        box_deprecation_warning(
            "to_dict", "DataDict", "Use dict(data_dict) instead."
        )  # pragma: nocover
        out_dict = dict(self)
        for k, v in out_dict.items():
            if v is self:
                out_dict[k] = out_dict
            elif isinstance(v, DataDict):
                out_dict[k] = v.to_dict()
            elif isinstance(v, DataList):
                out_dict[k] = v.to_list()
        return out_dict
```
[ ] f4b6a3--ulid-creator--compareTo
https://github.com/f4b6a3/ulid-creator/blob/1b82480604819c631a399ca173819de540fd1485/./src/main/java/com/github/f4b6a3/ulid/Ulid.java#L704-L737
```
	/**
	 * Compares two ULIDs as unsigned 128-bit integers.
	 * <p>
	 * The first of two ULIDs is greater than the second if the most significant
	 * byte in which they differ is greater for the first ULID.
	 * 
	 * @param that a ULID to be compared with
	 * @return -1, 0 or 1 as {@code this} is less than, equal to, or greater than
	 *         {@code that}
	 */
	@Override
	public int compareTo(Ulid that) {

		// used to compare as UNSIGNED longs
		final long min = 0x8000000000000000L;

		final long a = this.msb + min;
		final long b = that.msb + min;

		if (a > b)
			return 1;
		else if (a < b)
			return -1;

		final long c = this.lsb + min;
		final long d = that.lsb + min;

		if (c > d)
			return 1;
		else if (c < d)
			return -1;

		return 0;
	}
```
[ ] f4b6a3--ulid-creator--isValidCharArray
https://github.com/f4b6a3/ulid-creator/blob/1b82480604819c631a399ca173819de540fd1485/./src/main/java/com/github/f4b6a3/ulid/Ulid.java#L787-L824
```
	/*
	 * Checks if the string is a valid ULID.
	 * 
	 * A valid ULID string is a sequence of 26 characters from Crockford's Base 32
	 * alphabet.
	 * 
	 * The first character of the input string must be between 0 and 7.
	 */
	static boolean isValidCharArray(final char[] chars) {

		if (chars == null || chars.length != ULID_CHARS) {
			return false; // null or wrong size!
		}

		for (int i = 0; i < chars.length; i++) {
			try {
				if (ALPHABET_VALUES[chars[i]] == -1) {
					return false; // invalid character!
				}
			} catch (ArrayIndexOutOfBoundsException e) {
				return false; // Multibyte character!
			}
		}

		// The time component has 48 bits.
		// The base32 encoded time component has 50 bits.
		// The time component cannot be greater than than 2^48-1.
		// So the 2 first bits of the base32 decoded time component must be ZERO.
		// As a consequence, the 1st char of the input string must be between 0 and 7.
		if ((ALPHABET_VALUES[chars[0]] & 0b11000) != 0) {
			// ULID specification:
			// "Any attempt to decode or encode a ULID larger than this (time > 2^48-1)
			// should be rejected by all implementations, to prevent overflow bugs."
			return false; // time overflow!
		}

		return true; // It seems to be OK.
	}
```
[ ] f4b6a3--uuid-creator--expand
https://github.com/f4b6a3/uuid-creator/blob/3f41c3e6ed9fa3c229303672960570281f35a125/./src/main/java/com/github/f4b6a3/uuid/codec/base/BaseN.java#L284-L313
```
	/**
	 * Expands character sequences similar to 0-9, a-z and A-Z.
	 * 
	 * @param string a string to be expanded
	 * @return a string
	 */
	protected static String expand(String string) {

		StringBuilder buffer = new StringBuilder();

		int i = 1;
		while (i <= string.length()) {
			final char a = string.charAt(i - 1); // previous char
			if ((i < string.length() - 1) && (string.charAt(i) == '-')) {
				final char b = string.charAt(i + 1); // next char
				char[] expanded = expand(a, b);
				if (expanded.length != 0) {
					i += 2; // skip
					buffer.append(expanded);
				} else {
					buffer.append(a);
				}
			} else {
				buffer.append(a);
			}
			i++;
		}

		return buffer.toString();
	}
```
[ ] f4b6a3--uuid-creator--fromInts
https://github.com/f4b6a3/uuid-creator/blob/3f41c3e6ed9fa3c229303672960570281f35a125/./src/main/java/com/github/f4b6a3/uuid/util/internal/ByteUtil.java#L124-L152
```
	/**
	 * Converts an array of integers into an array of bytes. Each integer is decomposed into 4 bytes,
	 * with the most significant byte being placed first. This method produces a byte array of length 16,
	 * assuming the input array contains exactly 4 integers. The conversion is performed by shifting
	 * and masking operations to extract each byte from the integers.
	 *
	 * @param ints An array of integers to be converted into bytes. This array should contain exactly 4 integers.
	 * @return A byte array of length 16, where each group of 4 bytes represents one of the integers from the input array.
	 */
	public static byte[] fromInts(int[] ints) {
		byte[] bytes = new byte[16]; 
		bytes[0x0] = (byte) (ints[0] >>> 24);
		bytes[0x1] = (byte) (ints[0] >>> 16);
		bytes[0x2] = (byte) (ints[0] >>> 8);
		bytes[0x3] = (byte) (ints[0]);
		bytes[0x4] = (byte) (ints[1] >>> 24);
		bytes[0x5] = (byte) (ints[1] >>> 16);
		bytes[0x6] = (byte) (ints[1] >>> 8);
		bytes[0x7] = (byte) (ints[1]);
		bytes[0x8] = (byte) (ints[2] >>> 24);
		bytes[0x9] = (byte) (ints[2] >>> 16);
		bytes[0xa] = (byte) (ints[2] >>> 8);
		bytes[0xb] = (byte) (ints[2]);
		bytes[0xc] = (byte) (ints[3] >>> 24);
		bytes[0xd] = (byte) (ints[3] >>> 16);
		bytes[0xe] = (byte) (ints[3] >>> 8);
		bytes[0xf] = (byte) (ints[3]);
		return bytes;
	}
```
[ ] f4b6a3--uuid-creator--opaqueCompare
https://github.com/f4b6a3/uuid-creator/blob/3f41c3e6ed9fa3c229303672960570281f35a125/./src/main/java/com/github/f4b6a3/uuid/util/UuidComparator.java#L125-L178
```
	/**
	 * Compares two UUIDs.
	 * <p>
	 * The opaque static method compares two UUIDs as unsigned 128-bit integers.
	 * It's the same as lexicographic sorting of UUID canonical strings.
	 * <p>
	 * The first of two UUIDs is greater than the second if the most significant
	 * byte in which they differ is greater for the first UUID.
	 * <p>
	 * The opaque method is faster than the default method as it does not check the
	 * UUID version.
	 * <p>
	 * It's referred to as "opaque" just because it works like a "blind byte-to-byte
	 * comparison".
	 * <p>
	 * It can be useful for these reasons:
	 * <ol>
	 * <li>{@link UUID#compareTo(UUID)} can lead to unexpected behavior due to
	 * signed {@code long} comparison;
	 * <li>{@link UUID#compareTo(UUID)} throws {@link NullPointerException} if a
	 * {@code null} UUID is given.
	 * </ol>
	 * 
	 * @param uuid1 a {@code UUID}
	 * @param uuid2 another {@code UUID}
	 * @return -1, 0 or 1 as {@code u1} is less than, equal to, or greater than
	 *         {@code u2}
	 */
	public static int opaqueCompare(UUID uuid1, UUID uuid2) {

		UUID u1 = uuid1 != null ? uuid1 : new UUID(0L, 0L);
		UUID u2 = uuid2 != null ? uuid2 : new UUID(0L, 0L);

		// used to compare as UNSIGNED longs
		final long min = 0x8000000000000000L;

		final long a = u1.getMostSignificantBits() + min;
		final long b = u2.getMostSignificantBits() + min;

		if (a > b)
			return 1;
		else if (a < b)
			return -1;

		final long c = u1.getLeastSignificantBits() + min;
		final long d = u2.getLeastSignificantBits() + min;

		if (c > d)
			return 1;
		else if (c < d)
			return -1;

		return 0;
	}
```
[ ] f4b6a3--uuid-creator--selectNodeIdFunction
https://github.com/f4b6a3/uuid-creator/blob/3f41c3e6ed9fa3c229303672960570281f35a125/./src/main/java/com/github/f4b6a3/uuid/factory/AbstTimeBasedFactory.java#L209-L254
```
	/**
	 * Select the node identifier function.
	 * 
	 * This method reads the system property 'uuidcreator.node' and the environment
	 * variable 'UUIDCREATOR_NODE' to decide what node identifier function must be
	 * used.
	 * 
	 * 1. If it finds the string "mac", the generator will use the MAC address.
	 * 
	 * 2. If it finds the string "hash", the generator will use the system data
	 * hash.
	 * 
	 * 3. If it finds the string "random", the generator will use a random number
	 * that always changes.
	 * 
	 * 4. If it finds the string representation of a specific number in octal,
	 * hexadecimal or decimal format, the generator will use the number represented.
	 * 
	 * 5. Else, a random number will be used by the generator.
	 * 
	 * @return a node function
	 */
	protected static NodeIdFunction selectNodeIdFunction() {

		String string = SettingsUtil.getProperty(SettingsUtil.PROPERTY_NODE);

		if (NODE_MAC.equalsIgnoreCase(string)) {
			return new MacNodeIdFunction();
		}

		if (NODE_HASH.equalsIgnoreCase(string)) {
			return new HashNodeIdFunction();
		}

		if (NODE_RANDOM.equalsIgnoreCase(string)) {
			return new RandomNodeIdFunction();
		}

		Long number = SettingsUtil.getNodeIdentifier();
		if (number != null) {
			final long nodeid = NodeIdFunction.toExpectedRange(number);
			return () -> nodeid;
		}

		return new DefaultNodeIdFunction();
	}
```
[ ] f4b6a3--uuid-creator--toAndFromDotNetGuid
https://github.com/f4b6a3/uuid-creator/blob/3f41c3e6ed9fa3c229303672960570281f35a125/./src/main/java/com/github/f4b6a3/uuid/codec/other/DotNetGuid1Codec.java#L91-L129
```
	/**
	 * Convert a UUID to and from a .Net Guid.
	 * <p>
	 * It rearranges the most significant bytes from big-endian to little-endian,
	 * and vice-versa.
	 * <p>
	 * The .Net Guid stores the most significant bytes as little-endian, while the
	 * least significant bytes are stored as big-endian (network order).
	 * 
	 * @see <a href=
	 *      "https://blogs.msdn.microsoft.com/dbrowne/2012/07/03/how-to-generate-sequential-guids-for-sql-server-in-net/">How
	 *      to Generate Sequential GUIDs for SQL Server in .NET</a>
	 * @see <a href=
	 *      "http://sqlblog.com/blogs/alberto_ferrari/archive/2007/08/31/how-are-guids-sorted-by-sql-server.aspx">How
	 *      are GUIDs sorted by SQL Server?</a>
	 * 
	 * @param uuid a UUID
	 * @return another UUID
	 */
	protected static UUID toAndFromDotNetGuid(UUID uuid) {

		long msb = uuid.getMostSignificantBits();
		long lsb = uuid.getLeastSignificantBits();

		long newMsb = 0x0000000000000000L;
		// high bits
		newMsb |= (msb & 0xff000000_0000_0000L) >>> 24;
		newMsb |= (msb & 0x00ff0000_0000_0000L) >>> 8;
		newMsb |= (msb & 0x0000ff00_0000_0000L) << 8;
		newMsb |= (msb & 0x000000ff_0000_0000L) << 24;
		// mid bits
		newMsb |= (msb & 0x00000000_ff00_0000L) >>> 8;
		newMsb |= (msb & 0x00000000_00ff_0000L) << 8;
		// low bits
		newMsb |= (msb & 0x00000000_0000_ff00L) >>> 8;
		newMsb |= (msb & 0x00000000_0000_00ffL) << 8;

		return new UUID(newMsb, lsb);
	}
```
[ ] falconry--falcon--_parse_cookie_header
https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/request_helpers.py#L45-L103
```
def _parse_cookie_header(header_value: str) -> Dict[str, List[str]]:
    """Parse a Cookie header value into a dict of named values.

    (See also: RFC 6265, Section 5.4)

    Args:
        header_value (str): Value of a Cookie header

    Returns:
        dict: Map of cookie names to a list of all cookie values found in the
        header for that name. If a cookie is specified more than once in the
        header, the order of the values will be preserved.
    """

    # See also:
    #
    #   https://tools.ietf.org/html/rfc6265#section-5.4
    #   https://tools.ietf.org/html/rfc6265#section-4.1.1
    #

    cookies: Dict[str, List[str]] = {}

    for token in header_value.split(';'):
        name, __, value = token.partition('=')

        # NOTE(kgriffs): RFC6265 is more strict about whitespace, but we
        # are more lenient here to better handle old user agents and to
        # mirror Python's standard library cookie parsing behavior
        name = name.strip()
        value = value.strip()

        # NOTE(kgriffs): Skip malformed cookie-pair
        if not name:
            continue

        # NOTE(kgriffs): Skip cookies with invalid names
        if _COOKIE_NAME_RESERVED_CHARS.search(name):
            continue

        # NOTE(kgriffs): To maximize compatibility, we mimic the support in the
        # standard library for escaped characters within a double-quoted
        # cookie value according to the obsolete RFC 2109. However, we do not
        # expect to see this encoding used much in practice, since Base64 is
        # the current de-facto standard, as recommended by RFC 6265.
        #
        # PERF(kgriffs): These checks have been hoisted from within _unquote()
        # to avoid the extra function call in the majority of the cases when it
        # is not needed.
        if len(value) > 2 and value[0] == '"' and value[-1] == '"':
            value = http_cookies._unquote(value)

        # PERF(kgriffs): This is slightly more performant as
        # compared to using dict.setdefault()
        if name in cookies:
            cookies[name].append(value)
        else:
            cookies[name] = [value]

    return cookies
```
[ ] falconry--falcon--_parse_forwarded_header
https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/forwarded.py#L93-L192
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
[ ] falconry--falcon--_parse_header_old_stdlib
https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/util/mediatypes.py#L42-L63
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
[ ] falconry--falcon--capture_responder_args
https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/testing/resource.py#L40-L78
```
def capture_responder_args(
    req: wsgi.Request,
    resp: wsgi.Response,
    resource: object,
    params: typing.Mapping[str, str],
) -> None:
    """Before hook for capturing responder arguments.

    Adds the following attributes to the hooked responder's resource
    class:

        * `captured_req`
        * `captured_resp`
        * `captured_kwargs`

    In addition, if the capture-req-body-bytes header is present in the
    request, the following attribute is added:

        * `captured_req_body`

    Including the capture-req-media header in the request (set to any
    value) will add the following attribute:

        * `capture-req-media`
    """

    simple_resource = typing.cast(SimpleTestResource, resource)
    simple_resource.captured_req = req
    simple_resource.captured_resp = resp
    simple_resource.captured_kwargs = params

    simple_resource.captured_req_media = None
    simple_resource.captured_req_body = None

    num_bytes = req.get_header('capture-req-body-bytes')
    if num_bytes:
        simple_resource.captured_req_body = req.stream.read(int(num_bytes))
    elif req.get_header('capture-req-media'):
        simple_resource.captured_req_media = req.get_media()
```
[ ] falconry--falcon--process_response
https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/middleware.py#L103-L163
```
    def process_response(
        self, req: Request, resp: Response, resource: object, req_succeeded: bool
    ) -> None:
        """Implement the CORS policy for all routes.

        This middleware provides a simple out-of-the box CORS policy,
        including handling of preflighted requests from the browser.

        See also: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

        See also: https://www.w3.org/TR/cors/#resource-processing-model
        """

        origin = req.get_header('Origin')
        if origin is None:
            return

        if self.allow_origins != '*' and origin not in self.allow_origins:
            return

        if resp.get_header('Access-Control-Allow-Origin') is None:
            set_origin = '*' if self.allow_origins == '*' else origin
            if self.allow_credentials == '*' or origin in self.allow_credentials:
                set_origin = origin
                resp.set_header('Access-Control-Allow-Credentials', 'true')
            resp.set_header('Access-Control-Allow-Origin', set_origin)

        if self.expose_headers:
            resp.set_header('Access-Control-Expose-Headers', self.expose_headers)

        if (
            req_succeeded
            and req.method == 'OPTIONS'
            and req.get_header('Access-Control-Request-Method')
        ):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers', default='*'
            )

            if allow is None:
                # there is no allow set, remove all access control headers
                resp.delete_header('Access-Control-Allow-Methods')
                resp.delete_header('Access-Control-Allow-Headers')
                resp.delete_header('Access-Control-Max-Age')
                resp.delete_header('Access-Control-Expose-Headers')
                resp.delete_header('Access-Control-Allow-Origin')
            else:
                resp.set_header('Access-Control-Allow-Methods', allow)
                resp.set_header('Access-Control-Allow-Headers', allow_headers)
                resp.set_header('Access-Control-Max-Age', '86400')  # 24 hours

            if self.allow_private_network and (
                req.get_header('Access-Control-Request-Private-Network') == 'true'
            ):
                resp.set_header('Access-Control-Allow-Private-Network', 'true')
```
[ ] falconry--falcon--relative_uri
https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/request.py#L748-L761
```
    @property
    def relative_uri(self) -> str:
        """The path and query string portion of the
        request URI, omitting the scheme and host.
        """  # noqa: D205
        if self._cached_relative_uri is None:
            if self.query_string:
                self._cached_relative_uri = (
                    self.root_path + self.path + '?' + self.query_string
                )
            else:
                self._cached_relative_uri = self.root_path + self.path

        return self._cached_relative_uri
```
[ ] falconry--falcon--set_resp_defaults
https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/testing/resource.py#L107-L129
```
def set_resp_defaults(
    req: wsgi.Request,
    resp: wsgi.Response,
    resource: Resource,
    params: typing.Mapping[str, str],
) -> None:
    """Before hook for setting default response properties.

    This hook simply sets the the response body, status,
    and headers to the `_default_status`,
    `_default_body`, and `_default_headers` attributes
    that are assumed to be defined on the resource
    object.
    """
    simple_resource = typing.cast(SimpleTestResource, resource)
    if simple_resource._default_status is not None:
        resp.status = simple_resource._default_status

    if simple_resource._default_body is not None:
        resp.text = simple_resource._default_body

    if simple_resource._default_headers is not None:
        resp.set_headers(simple_resource._default_headers)
```
[x] fast-pack--JavaFastPFOR--uncompress-2
https://github.com/fast-pack/JavaFastPFOR/blob/922d46c2a28598c22a4729df0dba5b71eef498b7/./src/main/java/me/lemire/longcompression/LongAs2IntsCodec.java#L109-L187
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
[ ] flipkart-incubator--zjsonpatch--introduceExplicitRemoveAndAddOperation
https://github.com/flipkart-incubator/zjsonpatch/blob/334b66a2d20e32edb09ee17ab416e1b311feb7e3/./src/main/java/com/flipkart/zjsonpatch/JsonDiff.java#L228-L246
```
    /**
     * This method splits a {@link Operation#REPLACE} operation within a diff into a {@link Operation#REMOVE}
     * and {@link Operation#ADD} in order, respectively.
     * Does nothing if {@link Operation#REPLACE} op does not contain a from value
     */
    private void introduceExplicitRemoveAndAddOperation() {
        List<Diff> updatedDiffs = new ArrayList<Diff>();
        for (Diff diff : diffs) {
            if (!diff.getOperation().equals(Operation.REPLACE) || diff.getSrcValue() == null) {
                updatedDiffs.add(diff);
                continue;
            }
            //Split into two #REMOVE and #ADD
            updatedDiffs.add(new Diff(Operation.REMOVE, diff.getPath(), diff.getSrcValue()));
            updatedDiffs.add(new Diff(Operation.ADD, diff.getPath(), diff.getValue()));
        }
        diffs.clear();
        diffs.addAll(updatedDiffs);
    }
```
[ ] fronzbot--blinkpy--__init__
https://github.com/fronzbot/blinkpy/blob/1e868e2a19fa8b364f4e9164d1e31e7e4969c7fb/./blinkpy/auth.py#L28-L68
```
    def __init__(
        self,
        login_data=None,
        no_prompt=False,
        session=None,
        agent=DEFAULT_USER_AGENT,
        app_build=APP_BUILD,
        callback=None,
    ):
        """
        Initialize auth handler.

        :param login_data: dictionary for login data
                           must contain the following:
                             - username
                             - password
        :param no_prompt: Should any user input prompts
                          be suppressed? True/FALSE
        """
        if login_data is None:
            login_data = {}
        self.data = login_data
        self.token = login_data.get("token", None)
        self.expires_in = login_data.get("expires_in", None)
        self.expiration_date = login_data.get("expiration_date", None)
        self.refresh_token = login_data.get("refresh_token", None)
        self.host = login_data.get("host", None)
        self.region_id = login_data.get("region_id", None)
        self.client_id = login_data.get("client_id", None)
        self.account_id = login_data.get("account_id", None)
        self.user_id = login_data.get("user_id", None)
        self.login_response = None
        self.tier_info = None
        self.is_errored = False
        self.no_prompt = no_prompt
        self._agent = agent
        self._app_build = app_build
        self.session = session if session else ClientSession()

        # Callback to notify on token refresh
        self.callback = callback
```
[ ] frostming--marko--find_next
https://github.com/frostming/marko/blob/e2c502a0e0fa9b1b9de5135932c61593f7ea87f8/./marko/helpers.py#L57-L84
```
def find_next(
    text: str,
    target: Container[str],
    start: int = 0,
    end: int | None = None,
    disallowed: Container[str] = (),
) -> int:
    """Find the next occurrence of target in text, and return the index
    Characters are escaped by backslash.
    Optional disallowed characters can be specified, if found, the search
    will fail with -2 returned. Otherwise, -1 is returned if not found.
    """
    if end is None:
        end = len(text)
    i = start
    escaped = False
    while i < end:
        c = text[i]
        if escaped:
            escaped = False
        elif c in target:
            return i
        elif c in disallowed:
            return -2
        elif c == "\\":
            escaped = True
        i += 1
    return -1
```
[ ] frostming--marko--partition_by_spaces
https://github.com/frostming/marko/blob/e2c502a0e0fa9b1b9de5135932c61593f7ea87f8/./marko/helpers.py#L87-L105
```
def partition_by_spaces(text: str, spaces: str = " \t") -> tuple[str, str, str]:
    """Split the given text by spaces or tabs, and return a tuple of
    (start, delimiter, remaining). If spaces are not found, the latter
    two elements will be empty.
    """
    start = end = -1
    for i, c in enumerate(text):
        if c in spaces:
            if start >= 0:
                continue
            start = i
        elif start >= 0:
            end = i
            break
    if start < 0:
        return text, "", ""
    if end < 0:
        return text[:start], text[start:], ""
    return text[:start], text[start:end], text[end:]
```
[ ] fwkz--riposte--_process
https://github.com/fwkz/riposte/blob/174bded8ccd665556b163e5c5633d0900715740f/./riposte/riposte.py#L219-L231
```
    def _process(self) -> None:
        """Process input provided by the input stream.

        Get provided input, parse it, pick appropriate handling
        function and execute it.
        """
        user_input = next(self.input_stream)()
        if not user_input:
            return

        for line in self._split_inline_commands(user_input):
            command_name, *args = self._parse_line(line)
            self._get_command(command_name).execute(*args)
```
[ ] glytching--junit-extensions--getSystemProperties
https://github.com/glytching/junit-extensions/blob/5c498fd7a7a628e4d5f1c272c6bda24c8669d470/./src/main/java/io/github/glytching/junit/extension/system/SystemPropertyExtension.java#L207-L235
```
  /**
   * Get a collection of {@link SystemProperty} for the given {@code annotatedElement}. If the given
   * {@code annotatedElement} has no such annotations then an empty list is returned, if the given
   * {@code annotatedElement} is annotated with {@link SystemProperty} then a list with one element
   * is returned, if the given {@code annotatedElement} is annotated with {@link SystemProperties}
   * then a list with one element for each of the repeated {@link SystemProperty} values is
   * returned.
   *
   * <p>This is essentially a shortcut for logic such as: 'does this element have the {@link
   * SystemProperty} annotation, if not does it have the {@link SystemProperties}' followed by
   * gathering these annotation values.
   *
   * @param annotatedElement either a test class or a test method which may be annotated with a
   *     system property annotation
   * @return 0..* {@link SystemProperty} elements
   */
  private List<SystemProperty> getSystemProperties(AnnotatedElement annotatedElement) {
    List<SystemProperty> systemProperties = new ArrayList<>();
    if (isAnnotated(annotatedElement, SystemProperties.class)) {
      // gather the repeating system property values
      systemProperties.addAll(
          Arrays.asList(annotatedElement.getAnnotation(SystemProperties.class).value()));
    }
    if (isAnnotated(annotatedElement, SystemProperty.class)) {
      // add the single system property value
      systemProperties.add(annotatedElement.getAnnotation(SystemProperty.class));
    }
    return systemProperties;
  }
```
[ ] google--langextract--_assign_colors
https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/visualization.py#L179-L193
```
def _assign_colors(extractions: list[data.Extraction]) -> dict[str, str]:
  """Assigns a background colour to each extraction class.

  Args:
    extractions: list of extractions.

  Returns:
    Mapping from extraction_class to a hex colour string.
  """
  classes = {e.extraction_class for e in extractions if e.char_interval}
  color_map: dict[str, str] = {}
  palette_cycle = itertools.cycle(_PALETTE)
  for cls in sorted(classes):
    color_map[cls] = next(palette_cycle)
  return color_map
```
[ ] google--langextract--_is_sentence_break_after_newline
https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/core/tokenizer.py#L287-L324
```
def _is_sentence_break_after_newline(
    text: str,
    tokens: Sequence[Token],
    current_idx: int,
) -> bool:
  """Checks if there's a newline before the next token and if that next token starts uppercase.

  This is a heuristic for determining sentence boundaries. It favors terminating
  a sentence prematurely over missing a sentence boundary, and will terminate a
  sentence early if the first line ends with new line and the second line begins
  with a capital letter.

  Args:
    text: The entire input text.
    tokens: The sequence of Token objects.
    current_idx: The current token index.

  Returns:
    True if a newline is found between current_idx and current_idx+1, and
    the next token (if any) begins with an uppercase character.
  """
  if current_idx + 1 >= len(tokens):
    return False

  gap_text = text[
      tokens[current_idx]
      .char_interval.end_pos : tokens[current_idx + 1]
      .char_interval.start_pos
  ]
  if "\n" not in gap_text:
    return False

  next_token_text = text[
      tokens[current_idx + 1]
      .char_interval.start_pos : tokens[current_idx + 1]
      .char_interval.end_pos
  ]
  return bool(next_token_text) and next_token_text[0].isupper()
```
[ ] google--langextract--_kwargs_with_environment_defaults
https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/factory.py#L52-L87
```
def _kwargs_with_environment_defaults(
    model_id: str, kwargs: dict[str, typing.Any]
) -> dict[str, typing.Any]:
  """Add environment-based defaults to provider kwargs.

  Args:
    model_id: The model identifier.
    kwargs: Existing keyword arguments.

  Returns:
    Updated kwargs with environment defaults.
  """
  resolved = dict(kwargs)

  if "api_key" not in resolved:
    model_lower = model_id.lower()
    env_vars_by_provider = {
        "gemini": ("GEMINI_API_KEY", "LANGEXTRACT_API_KEY"),
        "gpt": ("OPENAI_API_KEY", "LANGEXTRACT_API_KEY"),
    }

    for provider_prefix, env_vars in env_vars_by_provider.items():
      if provider_prefix in model_lower:
        for env_var in env_vars:
          api_key = os.getenv(env_var)
          if api_key:
            resolved["api_key"] = api_key
            break
        break

  if "ollama" in model_id.lower() and "base_url" not in resolved:
    resolved["base_url"] = os.getenv(
        "OLLAMA_BASE_URL", "http://localhost:11434"
    )

  return resolved
```
[ ] google--langextract--format_extraction_example
https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/core/format_handler.py#L114-L147
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type == data.FormatType.YAML:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    return self._add_fences(formatted) if self.use_fences else formatted
```
[ ] google--langextract--requires_fence_output
https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/core/base_model.py#L86-L102
```
  @property
  def requires_fence_output(self) -> bool:
    """Whether this model requires fence output for parsing.

    Uses explicit override if set, otherwise computes from schema.
    Returns True if no schema or schema doesn't require raw output.
    """
    if (
        hasattr(self, '_fence_output_override')
        and self._fence_output_override is not None
    ):
      return self._fence_output_override

    schema_obj = self.schema
    if schema_obj is None:
      return True
    return not schema_obj.requires_raw_output
```
[ ] google--langextract--validate_format
https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/providers/schemas/gemini.py#L66-L95
```
  def validate_format(self, format_handler: fh.FormatHandler) -> None:
    """Validate Gemini's format requirements.

    Gemini requires:
    - No fence markers (outputs raw JSON via response_mime_type)
    - Wrapper with EXTRACTIONS_KEY (built into response_schema)
    """
    # Check for fence usage with raw JSON output
    if format_handler.use_fences:
      warnings.warn(
          "Gemini outputs native JSON via"
          " response_mime_type='application/json'. Using fence_output=True may"
          " cause parsing issues. Set fence_output=False.",
          UserWarning,
          stacklevel=3,
      )

    # Verify wrapper is enabled with correct key
    if (
        not format_handler.use_wrapper
        or format_handler.wrapper_key != data.EXTRACTIONS_KEY
    ):
      warnings.warn(
          "Gemini's response_schema expects"
          f" wrapper_key='{data.EXTRACTIONS_KEY}'. Current settings:"
          f" use_wrapper={format_handler.use_wrapper},"
          f" wrapper_key='{format_handler.wrapper_key}'",
          UserWarning,
          stacklevel=3,
      )
```
[ ] google--mobly--__init__
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_test.py#L183-L217
```
  def __init__(self, configs):
    """Constructor of BaseTestClass.

    The constructor takes a config_parser.TestRunConfig object and which has
    all the information needed to execute this test class, like log_path
    and controller configurations. For details, see the definition of class
    config_parser.TestRunConfig.

    Args:
      configs: A config_parser.TestRunConfig object.
    """
    self.tests = []
    class_identifier = self.__class__.__name__
    if configs.test_class_name_suffix:
      class_identifier = '%s_%s' % (
          class_identifier,
          configs.test_class_name_suffix,
      )
    if self.TAG is None:
      self.TAG = class_identifier
    # Set params.
    self.root_output_path = configs.log_path
    self.log_path = os.path.join(self.root_output_path, class_identifier)
    utils.create_dir(self.log_path)
    # Deprecated, use 'testbed_name'
    self.test_bed_name = configs.test_bed_name
    self.testbed_name = configs.testbed_name
    self.user_params = configs.user_params
    self.results = records.TestResult()
    self.summary_writer = configs.summary_writer
    self._generated_test_table = collections.OrderedDict()
    self._controller_manager = controller_manager.ControllerManager(
        class_name=self.TAG, controller_configs=configs.controller_configs
    )
    self.controller_configs = self._controller_manager.controller_configs
```
[ ] google--mobly--_count_eventually_passing_retries
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/records.py#L651-L668
```
  def _count_eventually_passing_retries(self):
    """Counts the number of retry iterations that eventually passed.

    If a test is retried and eventually passed, all the associated non-passing
    iterations should not be considered when devising the final state of the
    test run.

    Returns:
      Int, the number that should be subtracted from the result altering error
      counts.
    """
    count = 0
    for record in self.passed:
      r = record
      while r.parent is not None and r.parent[1] == TestParentType.RETRY:
        count += 1
        r = r.parent[0]
    return count
```
[ ] google--mobly--_exec_one_test_with_repeat
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_test.py#L711-L761
```
  def _exec_one_test_with_repeat(
      self, test_name, test_method, repeat_count, max_consecutive_error
  ):
    """Repeatedly execute a test case.

    This method performs the action defined by the `repeat` decorator.

    If the number of consecutive failures reach the threshold set by
    `max_consecutive_error`, the remaining iterations will be abandoned.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      repeat_count: int, the number of times to repeat the test case.
      max_consecutive_error: int, the maximum number of consecutive iterations
        allowed to fail before abandoning the remaining iterations.
    """

    consecutive_error_count = 0

    # If max_consecutive_error is not set by user, it is considered the same as
    # the repeat_count.
    if max_consecutive_error == 0:
      max_consecutive_error = repeat_count

    previous_record = None
    for i in range(repeat_count):
      new_test_name = f'{test_name}_{i}'
      new_record = records.TestResultRecord(new_test_name, self.TAG)
      if i > 0:
        new_record.parent = (previous_record, records.TestParentType.REPEAT)
      previous_record = self.exec_one_test(
          new_test_name, test_method, new_record
      )
      if previous_record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]:
        consecutive_error_count += 1
      else:
        consecutive_error_count = 0

      if consecutive_error_count == max_consecutive_error:
        logging.error(
            'Repeated test case "%s" has consecutively failed %d iterations, '
            'aborting the remaining %d iterations.',
            test_name,
            consecutive_error_count,
            repeat_count - 1 - i,
        )
        return
```
[ ] google--mobly--_exec_one_test_with_retry
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_test.py#L679-L709
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
[ ] google--mobly--_get_extras
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_instrumentation_test.py#L537-L566
```
  def _get_extras(self):
    """Gets the output for the extras section of the TestResultRecord.

    Returns:
      A string to set for a TestResultRecord's extras.
    """
    # Add empty line to start key-value pairs on a new line.
    extra_parts = ['']

    for value in self._unknown_keys.values():
      extra_parts.append(value)

    extra_parts.append(self._known_keys[_InstrumentationKnownStatusKeys.STREAM])
    extra_parts.append(
        self._known_keys[_InstrumentationKnownResultKeys.SHORTMSG]
    )
    extra_parts.append(
        self._known_keys[_InstrumentationKnownResultKeys.LONGMSG]
    )
    extra_parts.append(self._known_keys[_InstrumentationKnownStatusKeys.ERROR])

    if (
        self._known_keys[_InstrumentationKnownStatusKeys.STACK]
        not in self._known_keys[_InstrumentationKnownStatusKeys.STREAM]
    ):
      extra_parts.append(
          self._known_keys[_InstrumentationKnownStatusKeys.STACK]
      )

    return '\n'.join(filter(None, extra_parts))
```
[ ] google--mobly--_parse_line
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_instrumentation_test.py#L865-L883
```
  def _parse_line(self, instrumentation_block, line):
    """Parses an arbitrary line from the instrumentation output based upon
    the current parser state.

    Args:
      instrumentation_block: _InstrumentationBlock, an instrumentation
        block with any of the possible parser states.
      line: string, the raw instrumentation output line to parse
        appropriately.

    Returns:
      The next instrumenation block to continue parsing with.
    """
    if instrumentation_block.state == _InstrumentationBlockStates.METHOD:
      return self._parse_method_block_line(instrumentation_block, line)
    elif instrumentation_block.state == _InstrumentationBlockStates.RESULT:
      return self._parse_result_block_line(instrumentation_block, line)
    else:
      return self._parse_unknown_block_line(instrumentation_block, line)
```
[ ] google--mobly--_parse_raw_test_selector
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/suite_runner.py#L496-L556
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
[ ] google--mobly--_sanitize_windows_filename
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/logger.py#L294-L328
```
def _sanitize_windows_filename(filename):
  """Sanitizes a filename for Windows.

  Refer to the following Windows documentation page for the rules:
  https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file#naming-conventions

  If the filename matches one of Window's reserved file namespaces, then the
  `WINDOWS_RESERVED_FILENAME_PREFIX` (i.e. "mobly_") prefix will be appended
  to the filename to convert it into a valid Windows filename.

  Args:
    filename: string, the filename to sanitize for the Windows file system.

  Returns:
    A filename that should be safe to use on Windows.
  """
  if re.match(WINDOWS_RESERVED_FILENAME_REGEX, filename):
    return WINDOWS_RESERVED_FILENAME_PREFIX + filename

  filename = _truncate_filename(filename, WINDOWS_MAX_FILENAME_LENGTH)

  # In order to meet max length, none of these replacements should increase
  # the length of the filename.
  new_filename_chars = []
  for char in filename:
    if char in WINDOWS_RESERVED_CHARACTERS_REPLACEMENTS:
      new_filename_chars.append(WINDOWS_RESERVED_CHARACTERS_REPLACEMENTS[char])
    else:
      new_filename_chars.append(char)
  filename = ''.join(new_filename_chars)
  if filename.endswith('.') or filename.endswith(' '):
    # Filenames cannot end with a period or space on Windows.
    filename = filename[:-1] + '_'

  return filename
```
[ ] google--mobly--_setup_test_logger
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/logger.py#L163-L209
```
def _setup_test_logger(log_path, console_level, prefix=None):
  """Customizes the root logger for a test run.

  The logger object has a stream handler and a file handler. The stream
  handler logs INFO level to the terminal, the file handler logs DEBUG
  level to files.

  Args:
    log_path: Location of the log file.
    console_level: Log level threshold used for log messages printed
      to the console. Logs with a level less severe than
      console_level will not be printed to the console.
    prefix: A prefix for each log line in terminal.
    filename: Name of the log file. The default is the time the logger
      is requested.
  """
  log = logging.getLogger()
  kill_test_logger(log)
  log.propagate = False
  log.setLevel(logging.DEBUG)
  # Log info to stream
  terminal_format = log_line_format
  if prefix:
    terminal_format = '[%s] %s' % (prefix, log_line_format)
  c_formatter = logging.Formatter(terminal_format, log_line_time_format)
  ch = logging.StreamHandler(sys.stdout)
  ch.setFormatter(c_formatter)
  ch.setLevel(console_level)
  # Log everything to file
  f_formatter = logging.Formatter(log_line_format, log_line_time_format)
  # Write logger output to files
  fh_info = logging.FileHandler(
      os.path.join(log_path, records.OUTPUT_FILE_INFO_LOG)
  )
  fh_info.setFormatter(f_formatter)
  fh_info.setLevel(logging.INFO)
  fh_debug = logging.FileHandler(
      os.path.join(log_path, records.OUTPUT_FILE_DEBUG_LOG)
  )
  fh_debug.setFormatter(f_formatter)
  fh_debug.setLevel(logging.DEBUG)
  log.addHandler(ch)
  log.addHandler(fh_info)
  log.addHandler(fh_debug)
  log.log_path = log_path
  logging.log_path = log_path
  logging.root_output_path = log_path
```
[ ] google--mobly--_stop_port_forwarding
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/controllers/android_device_lib/snippet_client_v2.py#L722-L740
```
  def _stop_port_forwarding(self):
    """Stops the adb port forwarding used by this client.

    Although we explicitly forward and track the host port, it can be unforwarded
    unexpectedly due to flaky USB connections, adb restarts, or external tools
    (e.g., `adb forward --remove-all`). To prevent unnecessary errors, this method
    checks if the host port is still forwarded before attempting to remove it.
    """
    if self.host_port:
      occupied_ports = adb.list_occupied_adb_ports()
      if self.host_port not in occupied_ports:
        self.log.debug(
            'Host port %s is not currently forwarded by adb, skipping removal.',
            self.host_port,
        )
        self.host_port = None
        return
      self._device.adb.forward(['--remove', f'tcp:{self.host_port}'])
      self.host_port = None
```
[ ] google--mobly--add_record
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/records.py#L588-L609
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_FAIL:
      self.failed.append(record)
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.error.append(record)
```
[ ] google--mobly--add_value
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_instrumentation_test.py#L411-L432
```
  def add_value(self, line):
    """Adds unstructured or multi-line value output to the current parsed
    instrumentation block for outputting later.

    Usually, this will add extra lines to the value list for the current
    key-value pair. However, sometimes, such as when instrumentation
    failed to start, output does not follow the structured prefix format.
    In this case, adding all of the output is still useful so that a user
    can debug the issue.

    Args:
      line: string, the raw instrumentation line to append to the value
        list.
    """
    # Don't count whitespace only lines.
    if line.strip():
      self._empty = False

    if self.current_key in self.known_keys:
      self.known_keys[self.current_key].append(line)
    else:
      self.unknown_keys[self.current_key].append(line)
```
[x] google--mobly--cli_cmd_to_string
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/utils.py#L674-L686
```
def cli_cmd_to_string(args):
  """Converts a cmd arg list to string.

  Args:
    args: list of strings, the arguments of a command.

  Returns:
    String representation of the command.
  """
  if isinstance(args, str):
    # Return directly if it's already a string.
    return args
  return ' '.join([shlex.quote(arg) for arg in args])
```
[ ] google--mobly--create_output_excerpts
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/controllers/android_device_lib/services/logcat.py#L102-L139
```
  def create_output_excerpts(self, test_info):
    """Convenient method for creating excerpts of adb logcat.

    This copies logcat lines from self.adb_logcat_file_path to an excerpt
    file, starting from the location where the previous excerpt ended.

    Call this method at the end of: `setup_class`, `teardown_test`, and
    `teardown_class`.

    Args:
      test_info: `self.current_test_info` in a Mobly test.

    Returns:
      List of strings, the absolute paths to excerpt files.
    """
    dest_path = test_info.output_path
    utils.create_dir(dest_path)
    filename = self._ad.generate_filename(
        self.OUTPUT_FILE_TYPE, test_info, 'txt'
    )
    excerpt_file_path = os.path.join(dest_path, filename)
    with open(
        excerpt_file_path,
        'w',
        encoding='utf-8',
        errors='replace',
        # When newline is '', line endings are written without conversion.
        newline='',
    ) as out:
      # Devices may accidentally go offline during test,
      # check not None before readline().
      while self._adb_logcat_file_obj:
        line = self._adb_logcat_file_obj.readline()
        if not line:
          break
        out.write(line)
    self._ad.log.debug('logcat excerpt created at: %s', excerpt_file_path)
    return [excerpt_file_path]
```
[ ] google--mobly--filter_devices
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/controllers/android_device.py#L354-L370
```
def filter_devices(ads, func):
  """Finds the AndroidDevice instances from a list that match certain
  conditions.

  Args:
    ads: A list of AndroidDevice instances.
    func: A function that takes an AndroidDevice object and returns True
      if the device satisfies the filter condition.

  Returns:
    A list of AndroidDevice instances that satisfy the filter condition.
  """
  results = []
  for ad in ads:
    if func(ad):
      results.append(ad)
  return results
```
[ ] google--mobly--find_subclasses_in_module
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/utils.py#L704-L721
```
def find_subclasses_in_module(base_classes, module):
  """Finds the subclasses of the given classes in the given module.

  Args:
    base_classes: list of classes, the base classes to look for the
      subclasses of in the module.
    module: module, the module to look for the subclasses in.

  Returns:
    A list of all of the subclasses found in the module.
  """
  subclasses = []
  for _, module_member in module.__dict__.items():
    if inspect.isclass(module_member):
      for base_class in base_classes:
        if issubclass(module_member, base_class):
          subclasses.append(module_member)
  return subclasses
```
[ ] google--mobly--get_full_test_names
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/test_runner.py#L313-L339
```
  def get_full_test_names(self):
    """Returns the names of all tests that will be run in this test runner.

    Returns:
      A list of test names. Each test name is in the format of
      <test.TAG>.<test_name>.
    """
    test_names = []
    for test_run_info in self._test_run_infos:
      test_config = test_run_info.config.copy()
      test_config.test_class_name_suffix = test_run_info.test_class_name_suffix
      test = test_run_info.test_class(test_config)

      tests = self._get_test_names_from_class(test)
      if test_run_info.tests is not None:
        # If tests is provided, verify that all tests exist in the class.
        tests_set = set(tests)
        for test_name in test_run_info.tests:
          if test_name not in tests_set:
            raise Error(
                'Unknown test method: %s in class %s', (test_name, test.TAG)
            )
          test_names.append(f'{test.TAG}.{test_name}')
      else:
        test_names.extend([f'{test.TAG}.{n}' for n in tests])

    return test_names
```
[ ] google--mobly--getprops
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/controllers/android_device_lib/adb.py#L402-L431
```
  def getprops(self, prop_names):
    """Get multiple properties of the device.

    This is a convenience wrapper for `adb shell getprop`. Use this to
    reduce the number of adb calls when getting multiple properties.

    Args:
      prop_names: list of strings, the names of the properties to get.

    Returns:
      A dict containing name-value pairs of the properties requested, if
      they exist.
    """
    attempts = DEFAULT_GETPROPS_ATTEMPTS
    results = {}
    for attempt in range(attempts):
      # The ADB getprop command can randomly return empty string, so try
      # multiple times. This value should always be non-empty if the device
      # in a working state.
      raw_output = self.shell(['getprop'], timeout=DEFAULT_GETPROP_TIMEOUT_SEC)
      properties = self._parse_getprop_output(raw_output)
      if properties:
        for name in prop_names:
          if name in properties:
            results[name] = properties[name]
        break
      # Don't call sleep on the last attempt.
      if attempt < attempts - 1:
        time.sleep(DEFAULT_GETPROPS_RETRY_SLEEP_SEC)
    return results
```
[ ] google--mobly--parse_mobly_cli_args
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/test_runner.py#L90-L153
```
def parse_mobly_cli_args(argv):
  """Parses cli args that are consumed by Mobly.

  This is the arg parsing logic for the default test_runner.main entry point.

  Multiple arg parsers can be applied to the same set of cli input. So you
  can use this logic in addition to any other args you want to parse. This
  function ignores the args that don't apply to default `test_runner.main`.

  Args:
    argv: A list that is then parsed as cli args. If None, defaults to cli
      input.

  Returns:
    Namespace containing the parsed args.
  """
  parser = argparse.ArgumentParser(description='Mobly Test Executable.')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument(
      '-c',
      '--config',
      type=str,
      metavar='<PATH>',
      help='Path to the test configuration file.',
  )
  group.add_argument(
      '-l',
      '--list_tests',
      action='store_true',
      help=(
          'Print the names of the tests defined in a script without '
          'executing them.'
      ),
  )
  parser.add_argument(
      '--tests',
      '--test_case',
      nargs='+',
      type=str,
      metavar='[test_a test_b re:test_(c|d)...]',
      help=(
          'A list of tests in the test class to execute. Each value can be a '
          'test name string or a `re:` prefixed string for full regex match of'
          ' test names.'
      ),
  )
  parser.add_argument(
      '-tb',
      '--test_bed',
      nargs='+',
      type=str,
      metavar='[<TEST BED NAME1> <TEST BED NAME2> ...]',
      help='Specify which test beds to run tests on.',
  )

  parser.add_argument(
      '-v',
      '--verbose',
      action='store_true',
      help='Set console logger level to DEBUG',
  )
  if not argv:
    argv = sys.argv[1:]
  return parser.parse_known_args(argv)[0]
```
[ ] google--mobly--transition_state
https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_instrumentation_test.py#L434-L461
```
  def transition_state(self, new_state):
    """Transitions or sets the current instrumentation block to the new
    parser state.

    Args:
      new_state: _InstrumentationBlockStates, the state that the parser
        should transition to.

    Returns:
      A new instrumentation block set to the new state, representing
      the start of parsing a new instrumentation test method.
      Alternatively, if the current instrumentation block represents the
      start of parsing a new instrumentation block (state UNKNOWN), then
      this returns the current instrumentation block set to the now
      known parsing state.
    """
    if self.state == _InstrumentationBlockStates.UNKNOWN:
      self.state = new_state
      return self
    else:
      next_block = _InstrumentationBlock(
          state=new_state,
          prefix=self.prefix,
          previous_instrumentation_block=self,
      )
      if self.status_code in _InstrumentationStatusCodeCategories.TIMING:
        next_block.begin_time = self.begin_time
      return next_block
```
[ ] gouline--dbt-metabase--_scan_fields
https://github.com/gouline/dbt-metabase/blob/cf581fd3bbe9472d2aaa7ed5725b8c34372089cc/./dbtmetabase/manifest.py#L351-L371
```
    @staticmethod
    def _scan_fields(
        t: Mapping, fields: Iterable[str], ns: str
    ) -> MutableMapping[str, Any]:
        """Reads meta fields from a schem object.

        Args:
            t (Mapping): Target to scan for fields.
            fields (Iterable): List of fields to accept.
            ns (str): Field namespace (separated by .).

        Returns:
            Mapping: Field values.
        """

        vals = {}
        for field in fields:
            if f"{ns}.{field}" in t:
                value = t[f"{ns}.{field}"]
                vals[field] = value if value is not None else NullValue
        return vals
```
[ ] hynek--doc2dash--get_doctype
https://github.com/hynek/doc2dash/blob/a5fc14a6ee151eb1373733bed8d5f9adb2189795/./src/doc2dash/parsers/__init__.py#L17-L31
```
def get_doctype(
    path: Path,
) -> tuple[type[types.Parser], str] | tuple[None, None]:
    """
    Gets the appropriate doctype for *path*.

    Returns:
        Tuple of parser type and the name of the documentation.
    """
    for dt in DOCTYPES:
        name = dt.detect(path)
        if name:
            return dt, name
    else:
        return None, None
```
[ ] hynek--doc2dash--prepare_docset
https://github.com/hynek/doc2dash/blob/a5fc14a6ee151eb1373733bed8d5f9adb2189795/./src/doc2dash/docsets.py#L41-L101
```
def prepare_docset(
    source: Path,
    dest: Path,
    name: str,
    index_page: Path | None,
    enable_js: bool,
    online_redirect_url: str | None,
    playground_url: str | None,
    icon: Path | None,
    icon_2x: Path | None,
    full_text_search: FullTextSearch,
) -> DocSet:
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = dest / "Contents" / "Resources"
    docs = resources / "Documents"
    os.makedirs(resources)

    db_conn = sqlite3.connect(resources / "docSet.dsidx")
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = dest / "Contents" / "Info.plist"
    plist_cfg: dict[str, str | bool] = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "DashDocSetDeclaredInStyle": "originalName",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = str(index_page)
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url
    if playground_url is not None:
        plist_cfg["DashDocSetPlayURL"] = playground_url
    if full_text_search is FullTextSearch.FORBIDDEN:
        plist_cfg["DashDocSetFTSNotSupported"] = True
    if full_text_search is FullTextSearch.ON:
        plist_cfg["DashDocSetDefaultFTSEnabled"] = True

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    if icon:
        shutil.copy2(icon, dest / "icon.png")

    if icon_2x:
        shutil.copy2(icon_2x, dest / "icon@2x.png")

    return DocSet(path=dest, plist=plist_path, db_conn=db_conn)
```
[ ] javadev--LeetCode-in-Java--eraseOverlapIntervals
https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g0401_0500/s0435_non_overlapping_intervals/Solution.java#L9-L27
```
    /*
     * This is sorting my starting time, the key here is that we'll want to update end time when an
     * erasure is needed: we use the smaller end time instead of the bigger one which is more likely
     * to overlap with others.
     */
    public int eraseOverlapIntervals(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
        int erasures = 0;
        int end = intervals[0][1];
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] < end) {
                erasures++;
                end = Math.min(end, intervals[i][1]);
            } else {
                end = intervals[i][1];
            }
        }
        return erasures;
    }
```
[x] javadev--LeetCode-in-Java--evaluate
https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g2201_2300/s2232_minimize_result_by_adding_parentheses_to_expression/Solution.java#L58-L85
```
    /* This function is responsible for calculating the expressions of each variable.

    a = (0, left) // from the start of the expression to the first parentheses
    b = (left, right) // between parentheses, include plus sign
    c = (right, end of expression) // from the last parentheses to the end
    */
    private int evaluate(int left, int right, String expression) {
        // This means that the parentheses are at the beginning or end of the expression and are
        // equal to the range of the expression to be evaluated. Return 1 to avoid zero factors in
        // equation (a * b * c).
        if (left == right) {
            return 1;
        }
        int number = 0;
        for (int i = left; i < right; i++) {
            // If we find a sign, we must add both parts, therefore, we convert the expression to (a
            // + b).
            // We return the variable (a) wich is (number) and add to what follows after the sign (i
            // + 1).
            // We call the same function to calculate the b value.
            if (expression.charAt(i) == '+') {
                return number + evaluate(i + 1, right, expression);
            } else {
                number = (number * 10) + (expression.charAt(i) - '0');
            }
        }
        return number;
    }
```
[ ] javadev--LeetCode-in-Java--findMaxForm
https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g0401_0500/s0474_ones_and_zeroes/Solution.java#L7-L29
```
    /*
     * The problem can be interpreted as:
     * What's the max number of str can we pick from strs with limitation of m "0"s and n "1"s.
     *
     * Thus we can define dp[i][j] as it stands for max number of str can we pick from strs with limitation
     * of i "0"s and j "1"s.
     *
     * For each str, assume it has a "0"s and b "1"s, we update the dp array iteratively
     * and set dp[i][j] = Math.max(dp[i][j], dp[i - a][j - b] + 1).
     * So at the end, dp[m][n] is the answer.
     */
    public int findMaxForm(String[] strs, int m, int n) {
        int[][] dp = new int[m + 1][n + 1];
        for (String str : strs) {
            int[] count = count(str);
            for (int i = m; i >= count[0]; i--) {
                for (int j = n; j >= count[1]; j--) {
                    dp[i][j] = Math.max(dp[i][j], dp[i - count[0]][j - count[1]] + 1);
                }
            }
        }
        return dp[m][n];
    }
```
[x] javadev--LeetCode-in-Java--findMinArrowShots
https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g0401_0500/s0452_minimum_number_of_arrows_to_burst_balloons/Solution.java#L9-L31
```
    /*
     * I'm glad to have come up with this solution on my own on 10/13/2021:
     * we'll have to sort the
     * balloons by its ending points, a counter case to this is below:
     * {{0, 6}, {0, 9}, {7, 8}}
     * if we sort by starting points, then it becomes:
     * {0, 6}, {0, 9}, {7, 8}
     * this way, if we shoot 9,
     * {0, 6} won't be burst however, if we sort by ending points, then it becomes:
     * {0, 6}, {7, 8}, {0, 9}, then we shoot at 6, then at 8, this gives us the result of bursting all balloons.
     */
    public int findMinArrowShots(int[][] points) {
        Arrays.sort(points, (a, b) -> Integer.compare(a[1], b[1]));
        int minArrows = 1;
        long end = points[0][1];
        for (int i = 1; i < points.length; i++) {
            if (points[i][0] > end) {
                minArrows++;
                end = points[i][1];
            }
        }
        return minArrows;
    }
```
[ ] javadev--LeetCode-in-Java--findNthDigit
https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g0301_0400/s0400_nth_digit/Solution.java#L6-L24
```
    /*
     * 1. find the length of the number where the nth digit is from
     * 2. find the actual number where the nth digit is from
     * 3. find the nth digit and return
     */
    public int findNthDigit(int n) {
        int len = 1;
        long count = 9;
        int start = 1;
        while (n > len * count) {
            n -= (int) (len * count);
            len += 1;
            count *= 10;
            start *= 10;
        }
        start += (n - 1) / len;
        String s = Integer.toString(start);
        return Character.getNumericValue(s.charAt((n - 1) % len));
    }
```
[ ] javadev--LeetCode-in-Java--nextGreaterElement
https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g0501_0600/s0556_next_greater_element_iii/Solution.java#L7-L53
```
    /*
    - What this problem wants is finding the next permutation of n
    - Steps to find the next permuation:
       find largest index k such that inp[k] < inp[k+1];
           if k == -1: return -1
           else:
               look for largest index l such that inp[l] > inp[k]
               swap the two index
               reverse from k+1 to n.length
       */
    public int nextGreaterElement(int n) {
        char[] inp = String.valueOf(n).toCharArray();
        // Find k
        int k = -1;
        for (int i = inp.length - 2; i >= 0; i--) {
            if (inp[i] < inp[i + 1]) {
                k = i;
                break;
            }
        }
        if (k == -1) {
            return -1;
        }
        // Find l
        int largerIdx = inp.length - 1;
        for (int i = inp.length - 1; i >= 0; i--) {
            if (inp[i] > inp[k]) {
                largerIdx = i;
                break;
            }
        }
        swap(inp, k, largerIdx);
        reverse(inp, k + 1, inp.length - 1);
        // Build result
        int ret = 0;
        for (char c : inp) {
            int digit = c - '0';
            // Handle the case if ret > Integer.MAX_VALUE - This idea is borrowed from problem  8.
            // String to Integer (atoi)
            if (ret > Integer.MAX_VALUE / 10
                    || (ret == Integer.MAX_VALUE / 10 && digit > Integer.MAX_VALUE % 10)) {
                return -1;
            }
            ret = ret * 10 + (c - '0');
        }
        return ret;
    }
```
[ ] javadev--LeetCode-in-Java--remove
https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g0301_0400/s0380_insert_delete_getrandom_o1/RandomizedSet.java#L36-L49
```
    /* Removes a value from the set. Returns true if the set contained the specified element. */
    public boolean remove(int val) {
        if (!map.containsKey(val)) {
            return false;
        }
        int swap1 = map.get(val);
        int swap2 = list.size() - 1;
        int val2 = list.get(swap2);
        map.put(val2, swap1);
        map.remove(val);
        list.set(swap1, val2);
        list.remove(list.size() - 1);
        return true;
    }
```
[x] javadev--LeetCode-in-Java--sumSubseqWidths
https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g0801_0900/s0891_sum_of_subsequence_widths/Solution.java#L16-L47
```
    /*
        16+8+4+2+1(for 1 as min) 8+4+2+1(for 2 as min)  4+2+1(for 3 as min)  2+1(for 4 as min)  1(for 5 as min)
        -1*nums[0]*31 + nums[1]*1 + nums[2]*2 + nums[3]*4 + nums[4]*8 + nums[5]*16
            -1*nums[1]*15 + nums[2]*1 +nums[3]*2 + nums[4]*4 + nums[5]*8
            -1*nums[2]*7 + nums[3]*1 + nums[4]*2 + nums[5]*4
            -1*nums[3]*3 + nums[4]*1 + nums[5]*2
            -1*nums[4]*1 + nums[5]*1

            -nums[0]*31 + -nums[1]*15 - nums[2]*7 - nums[3]*3 - nums[4]*1
            nums[1]*1 + nums[2]*3 + nums[3]*7 + nums[4]*15 + nums[5]*31

        (-1)*nums[0]*(pow[6-1-0]-1) + (-1)*nums[1]*(pow[6-1-1]-1) + (-1)*nums[2]*(pow[6-1-2]-1)
        ... (-1)* nums[5]*(pow[6-1-5]-1)
        + nums[1]*(pow[1]-1) + nums[2]*(pow[2]-1) + .... + nums[5]*(pow[5]-1)

        (-1)*A[i]*(pow[l-1-i]-1) + A[i]*(pow[i]-1)
    */
    public int sumSubseqWidths(int[] nums) {
        int mod = 1_000_000_007;
        Arrays.sort(nums);
        int l = nums.length;
        long[] pow = new long[l];
        pow[0] = 1;
        for (int i = 1; i < l; i++) {
            pow[i] = pow[i - 1] * 2 % mod;
        }
        long res = 0;
        for (int i = 0; i < l; i++) {
            res = (res + (-1) * nums[i] * (pow[l - 1 - i] - 1) + nums[i] * (pow[i] - 1)) % mod;
        }
        return (int) res;
    }
```
[ ] jcbvm--i18n-editor--childKey
https://github.com/jcbvm/i18n-editor/blob/2c8b7b5afbf2a8963cad9400bf0954340a0accd3/./src/main/java/com/jvms/i18neditor/util/ResourceKeys.java#L127-L145
```
	/**
	 * Retrieve the part of the given key which is a child part of the given parent key.
	 * A key is a child of another key if it has the same parts at the beginning as the other key.
	 * This function will only return the child parts, so without the beginning parent parts.
	 * 
	 * <p>If the resulting key is the same as the given key, the key is considered not to be a child 
	 * of the given parent key, so an empty key will be returned.</p>
	 * 
	 * @param 	key the original key.
	 * @param 	parentKey a possible parent key of the original key.
	 * @return 	the part of the given key which is a child of the given parent key.
	 */
	public static String childKey(String key, String parentKey) {
		if (key == null || key.isEmpty()) return "";
		if (parentKey == null || parentKey.isEmpty()) return key;
		String result = key.replaceFirst(parentKey + "\\.", "");
		if (result.equals(key)) return "";
		return result;
	}
```
[ ] jhg023--SimpleNet--getSize
https://github.com/jhg023/SimpleNet/blob/08b1b52e0ca2612b9d38410cbf06eff032f6627f/./src/main/java/com/github/simplenet/packet/Packet.java#L437-L459
```
    /**
     * Gets the size of this {@link Packet packet}'s payload in bytes, while taking the specified {@link Client
     * client}'s encryption into account, as a {@link Cipher cipher}'s padding may increase the size of this
     * {@link Packet packet}.
     *
     * @param client The {@link Client client} that this {@link Packet packet}'s size should be calculated for.
     * @return The current size of this {@link Packet packet} in bytes.
     */
    public int getSize(Client client) {
        Cipher encryptionCipher;
        
        if (client == null || (encryptionCipher = client.getEncryptionCipher()) == null) {
            return size;
        }

        if (!client.isEncryptionNoPadding()) {
            int blockSize = encryptionCipher.getBlockSize();
            return Utility.roundUpToNextMultiple(size, blockSize == 0 ?
                encryptionCipher.getOutputSize(size) : blockSize);
        }
        
        return size;
    }
```
[x] jhy--jsoup--addAll
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Attributes.java#L360-L377
```
    /**
     Add all the attributes from the incoming set to this set.
     @param incoming attributes to add to these attributes.
     */
    public void addAll(Attributes incoming) {
        int incomingSize = incoming.size(); // not adding internal
        if (incomingSize == 0) return;
        checkCapacity(size + incomingSize);

        boolean needsPut = size != 0; // if this set is empty, no need to check existing set, so can add() vs put()
        // (and save bashing on the indexOfKey()
        for (Attribute attr : incoming) {
            if (needsPut)
                put(attr);
            else
                addObject(attr.getKey(), attr.getValue());
        }
    }
```
[ ] jhy--jsoup--asString
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/helper/W3CDom.java#L100-L148
```
    /**
     * Serialize a W3C document to a String. Provide Properties to define output settings including if HTML or XML. If
     * you don't provide the properties ({@code null}), the output will be auto-detected based on the content of the
     * document.
     *
     * @param doc Document
     * @param properties (optional/nullable) the output properties to use. See {@link
     *     Transformer#setOutputProperties(Properties)} and {@link OutputKeys}
     * @return Document as string
     * @see #OutputHtml
     * @see #OutputXml
     * @see OutputKeys#ENCODING
     * @see OutputKeys#OMIT_XML_DECLARATION
     * @see OutputKeys#STANDALONE
     * @see OutputKeys#DOCTYPE_PUBLIC
     * @see OutputKeys#CDATA_SECTION_ELEMENTS
     * @see OutputKeys#INDENT
     * @see OutputKeys#MEDIA_TYPE
     */
    public static String asString(Document doc, @Nullable Map<String, String> properties) {
        try {
            DOMSource domSource = new DOMSource(doc);
            StringWriter writer = new StringWriter();
            StreamResult result = new StreamResult(writer);
            TransformerFactory tf = TransformerFactory.newInstance();
            Transformer transformer = tf.newTransformer();
            if (properties != null)
                transformer.setOutputProperties(propertiesFromMap(properties));

            if (doc.getDoctype() != null) {
                DocumentType doctype = doc.getDoctype();
                if (!StringUtil.isBlank(doctype.getPublicId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC, doctype.getPublicId());
                if (!StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, doctype.getSystemId());
                    // handle <!doctype html> for legacy dom.
                else if (doctype.getName().equalsIgnoreCase("html")
                    && StringUtil.isBlank(doctype.getPublicId())
                    && StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "about:legacy-compat");
            }

            transformer.transform(domSource, result);
            return writer.toString();

        } catch (TransformerException e) {
            throw new IllegalStateException(e);
        }
    }
```
[ ] jhy--jsoup--body
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Document.java#L145-L163
```
    /**
     Get this document's {@code <body>} or {@code <frameset>} element.
     <p>
     As a <b>side-effect</b>, if this Document does not already have an HTML structure, it will be created with a {@code
    <body>} element. If you do not want that, use {@code #selectFirst("body")} instead.

     @return {@code body} element for documents with a {@code <body>}, a new {@code <body>} element if the document
     had no contents, or the outermost {@code <frameset> element} for frameset documents.
     */
    public Element body() {
        final Element html = htmlEl();
        Element el = html.firstElementChild();
        while (el != null) {
            if (el.nameIs("body") || el.nameIs("frameset"))
                return el;
            el = el.nextElementSibling();
        }
        return html.appendElement("body");
    }
```
[ ] jhy--jsoup--cachedChildren
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Element.java#L422-L437
```
    /** returns the cached child els, if they exist, and the modcount of our childnodes matches the stashed modcount */
    @Nullable List<Element> cachedChildren() {
        if (attributes == null || !attributes.hasUserData()) return null; // don't create empty userdata
        Map<String, Object> userData = attributes.userData();
        //noinspection unchecked
        WeakReference<List<Element>> ref = (WeakReference<List<Element>>) userData.get(childElsKey);
        if (ref != null) {
            List<Element> els = ref.get();
            if (els != null) {
                Integer modCount = (Integer) userData.get(childElsMod);
                if (modCount != null && modCount == childNodes.modCount())
                    return els;
            }
        }
        return null;
    }
```
[ ] jhy--jsoup--childElementsList
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Element.java#L402-L417
```
    /**
     * Maintains a shadow copy of this element's child elements. If the nodelist is changed, this cache is invalidated.
     * @return a list of child elements
     */
    List<Element> childElementsList() {
        if (childNodeSize() == 0) return EmptyChildren; // short circuit creating empty
        // set atomically, so works in multi-thread. Calling methods look like reads, so should be thread-safe
        synchronized (childNodes) { // sync vs re-entrant lock, to save another field
            List<Element> children = cachedChildren();
            if (children == null) {
                children = filterNodes(Element.class);
                stashChildren(children);
            }
            return children;
        }
    }
```
[ ] jhy--jsoup--clean
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/Jsoup.java#L335-L355
```
    /**
     Get safe HTML from untrusted input HTML, by parsing input HTML and filtering it through an allow-list of safe
     tags and attributes.

     @param bodyHtml  input untrusted HTML (body fragment)
     @param baseUri   URL to resolve relative URLs against
     @param safelist  list of permitted HTML elements
     @return safe HTML (body fragment)

     @see Cleaner#clean(Document)
     */
    public static String clean(String bodyHtml, String baseUri, Safelist safelist) {
        if (baseUri.isEmpty() && safelist.preserveRelativeLinks()) {
            baseUri = DummyUri; // set a placeholder URI to allow relative links to pass abs resolution for protocol tests; won't leak to output
        }

        Document dirty = parseBodyFragment(bodyHtml, baseUri);
        Cleaner cleaner = new Cleaner(safelist);
        Document clean = cleaner.clean(dirty);
        return clean.body().html();
    }
```
[ ] jhy--jsoup--closest
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Element.java#L749-L766
```
    /**
     * Find the closest element up the tree of parents that matches the specified evaluator. Will return itself, an
     * ancestor, or {@code null} if there is no such matching element.
     * @param evaluator a query evaluator
     * @return the closest ancestor element (possibly itself) that matches the provided evaluator. {@code null} if not
     * found.
     */
    public @Nullable Element closest(Evaluator evaluator) {
        Validate.notNull(evaluator);
        Element el = this;
        final Element root = root();
        do {
            if (evaluator.matches(root, el))
                return el;
            el = el.parent();
        } while (el != null);
        return null;
    }
```
[ ] jhy--jsoup--consumeTo
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/parser/CharacterReader.java#L374-L398
```
    /**
     Reads the characters up to (but not including) the specified case-sensitive string.
     <p>If the sequence is not found in the buffer, will return the remainder of the current buffered amount, less the
     length of the sequence, such that this call may be repeated.
     @param seq the delimiter
     @return the chars read
     */
    public String consumeTo(String seq) {
        int offset = nextIndexOf(seq);
        if (offset != -1) {
            String consumed = cacheString(charBuf, stringCache, bufPos, offset);
            bufPos += offset;
            return consumed;
        } else if (bufLength - bufPos < seq.length()) {
            // nextIndexOf() did a bufferUp(), so if the buffer is shorter than the search string, we must be at EOF
            return consumeToEnd();
        } else {
            // the string we're looking for may be straddling a buffer boundary, so keep (length - 1) characters
            // unread in case they contain the beginning of the search string
            int endPos = bufLength - seq.length() + 1;
            String consumed = cacheString(charBuf, stringCache, bufPos, endPos - bufPos);
            bufPos = endPos;
            return consumed;
        }
    }
```
[ ] jhy--jsoup--containsIgnoreCase
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/parser/CharacterReader.java#L609-L628
```
    /** Used to check presence of </title>, </style> when we're in RCData and see a <xxx. Only finds consistent case. */
    boolean containsIgnoreCase(String seq) {
        if (seq.equals(lastIcSeq)) {
            if (lastIcIndex == -1) return false;
            if (lastIcIndex >= bufPos) return true;
        }
        lastIcSeq = seq;

        String loScan = seq.toLowerCase(Locale.ENGLISH);
        int lo = nextIndexOf(loScan);
        if (lo > -1) {
            lastIcIndex = bufPos + lo; return true;
        }

        String hiScan = seq.toUpperCase(Locale.ENGLISH);
        int hi = nextIndexOf(hiScan);
        boolean found = hi > -1;
        lastIcIndex = found ? bufPos + hi : -1; // we don't care about finding the nearest, just that buf contains
        return found;
    }
```
[ ] jhy--jsoup--convert
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/helper/W3CDom.java#L237-L258
```
    /**
     * Converts a jsoup element into the provided W3C Document. If required, you can set options on the output
     * document before converting.
     *
     * @param in jsoup element
     * @param out w3c doc
     * @see org.jsoup.helper.W3CDom#fromJsoup(org.jsoup.nodes.Element)
     */
    public void convert(org.jsoup.nodes.Element in, Document out) {
        W3CBuilder builder = new W3CBuilder(out);
        builder.namespaceAware = namespaceAware;
        org.jsoup.nodes.Document inDoc = in.ownerDocument();
        if (inDoc != null) {
            if (!StringUtil.isBlank(inDoc.location())) {
                out.setDocumentURI(inDoc.location());
            }
            builder.syntax = inDoc.outputSettings().syntax();
        }
        org.jsoup.nodes.Element rootEl = in instanceof org.jsoup.nodes.Document ? in.firstElementChild() : in; // skip the #root node if a Document
        assert rootEl != null;
        builder.traverse(rootEl);
    }
```
[ ] jhy--jsoup--cssSelector
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Element.java#L1106-L1133
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
[ ] jhy--jsoup--eachAttr
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/select/Elements.java#L106-L120
```
    /**
     * Get the attribute value for each of the matched elements. If an element does not have this attribute, no value is
     * included in the result set for that element.
     * @param attributeKey the attribute name to return values for. You can add the {@code abs:} prefix to the key to
     * get absolute URLs from relative URLs, e.g.: {@code doc.select("a").eachAttr("abs:href")} .
     * @return a list of each element's attribute value for the attribute
     */
    public List<String> eachAttr(String attributeKey) {
        List<String> attrs = new ArrayList<>(size());
        for (Element element : this) {
            if (element.hasAttr(attributeKey))
                attrs.add(element.attr(attributeKey));
        }
        return attrs;
    }
```
[ ] jhy--jsoup--elements
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/FormElement.java#L38-L52
```
    /**
     * Get the list of form control elements associated with this form.
     * @return form controls associated with this element.
     */
    public Elements elements() {
        // As elements may have been added or removed from the DOM after parse, prepare a new list that unions them:
        Elements els = select(submittable); // current form children
        for (Element linkedEl : linkedEls) {
            if (linkedEl.ownerDocument() != null && !els.contains(linkedEl)) {
                els.add(linkedEl); // adds previously linked elements, that weren't previously removed from the DOM
            }
        }

        return els;
    }
```
[ ] jhy--jsoup--evalWantsSiblings
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/select/StructuralEvaluator.java#L117-L127
```
        /* Test if the :has sub-clause wants sibling elements (vs nested elements) - will be a Combining eval */
        private static boolean evalWantsSiblings(Evaluator eval) {
            if (eval instanceof CombiningEvaluator) {
                CombiningEvaluator ce = (CombiningEvaluator) eval;
                for (Evaluator innerEval : ce.evaluators) {
                    if (innerEval instanceof PreviousSibling || innerEval instanceof ImmediatePreviousSibling)
                        return true;
                }
            }
            return false;
        }
```
[x] jhy--jsoup--getCharsetFromContentType
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/helper/DataUtil.java#L352-L367
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
[ ] jhy--jsoup--hasChildBlocks
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Printer.java#L169-L180
```
        /**
         Returns true if any of the Element's child nodes should indent. Checks the last 5 nodes only (to minimize
         scans).
         */
        static boolean hasChildBlocks(Element el) {
            Element child = el.firstElementChild();
            for (int i = 0; i < maxScan && child != null; i++) {
                if (child.isBlock() || !child.tag.isKnownTag()) return true;
                child = child.nextElementSibling();
            }
            return false;
        }
```
[ ] jhy--jsoup--head
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Document.java#L126-L143
```
    /**
     Get this document's {@code head} element.
     <p>
     As a side effect, if this Document does not already have an HTML structure, it will be created. If you do not want
     that, use {@code #selectFirst("head")} instead.

     @return {@code head} element.
     */
    public Element head() {
        final Element html = htmlEl();
        Element el = html.firstElementChild();
        while (el != null) {
            if (el.nameIs("head"))
                return el;
            el = el.nextElementSibling();
        }
        return html.prependElement("head");
    }
```
[ ] jhy--jsoup--isBlank
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/internal/StringUtil.java#L146-L161
```
    /**
     * Tests if a string is blank: null, empty, or only whitespace (" ", \r\n, \t, etc)
     * @param string string to test
     * @return if string is blank
     */
    public static boolean isBlank(@Nullable String string) {
        if (string == null || string.isEmpty())
            return true;

        int l = string.length();
        for (int i = 0; i < l; i++) {
            if (!StringUtil.isWhitespace(string.codePointAt(i)))
                return false;
        }
        return true;
    }
```
[ ] jhy--jsoup--maybeAddUndeclaredNs
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/helper/W3CDom.java#L428-L458
```
        /**
         Add a namespace declaration for an attribute with a prefix if it is not already present. Ensures that attributes
         with prefixes have the corresponding namespace declared, E.g. attribute "v-bind:foo" gets another attribute
         "xmlns:v-bind='undefined'. So that the asString() transformation pass is valid.
         If the parser was HTML we don't have a discovered namespace but we are trying to coerce it, so walk up the
         element stack and find it.
         */
        private void maybeAddUndeclaredNs(String namespace, String attrKey, org.jsoup.nodes.Element jEl, Element wEl) {
            if (!namespaceAware || !namespace.isEmpty()) return;
            int pos = attrKey.indexOf(':');
            if (pos != -1) { // prefixed but no namespace defined during parse, add a fake so that w3c serialization doesn't blow up
                String prefix = attrKey.substring(0, pos);
                if (prefix.equals("xmlns")) return;
                org.jsoup.nodes.Document doc = jEl.ownerDocument();
                if (doc != null && doc.parser().getTreeBuilder() instanceof HtmlTreeBuilder) {
                    // try walking up the stack and seeing if there is a namespace declared for this prefix (and that we didn't parse because HTML)
                    for (org.jsoup.nodes.Element el = jEl; el != null; el = el.parent()) {
                        String ns = el.attr("xmlns:" + prefix);
                        if (!ns.isEmpty()) {
                            namespace = ns;
                            // found it, set it
                            wEl.setAttributeNS(namespace, attrKey, jEl.attr(attrKey));
                            return;
                        }
                    }
                }

                // otherwise, put in a fake one
                wEl.setAttribute("xmlns:" + prefix, undefinedNs);
            }
        }
```
[ ] jhy--jsoup--maybeFindNext
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/NodeIterator.java#L79-L90
```
    /**
     If next is not null, looks for and sets next. If next is null after this, we have reached the end.
     */
    private void maybeFindNext() {
        if (next != null) return;

        //  change detected (removed or replaced), redo from previous
        if (currentParent != null && !current.hasParent())
            current = previous;

        next = findNextNode();
    }
```
[ ] jhy--jsoup--onStackNot
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/parser/HtmlTreeBuilder.java#L757-L769
```
    /** Tests if there is some element on the stack that is not in the provided set. */
    boolean onStackNot(String[] allowedTags) {
        final int bottom = stack.size() -1;
        final int top = bottom > MaxScopeSearchDepth ? bottom - MaxScopeSearchDepth : 0;
        // don't walk too far up the tree

        for (int pos = bottom; pos >= top; pos--) {
            final String elName = stack.get(pos).normalName();
            if (!inSorted(elName, allowedTags))
                return true;
        }
        return false;
    }
```
[ ] jhy--jsoup--padding
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/internal/StringUtil.java#L127-L144
```
    /**
     * Returns space padding, up to a max of maxPaddingWidth.
     * @param width amount of padding desired
     * @param maxPaddingWidth maximum padding to apply. Set to {@code -1} for unlimited.
     * @return string of spaces * width
     */
    public static String padding(int width, int maxPaddingWidth) {
        Validate.isTrue(width >= 0, "width must be >= 0");
        Validate.isTrue(maxPaddingWidth >= -1);
        if (maxPaddingWidth != -1)
            width = Math.min(width, maxPaddingWidth);
        if (width < padding.length)
            return padding[width];        
        char[] out = new char[width];
        for (int i = 0; i < width; i++)
            out[i] = ' ';
        return String.valueOf(out);
    }
```
[ ] jhy--jsoup--previousElementSibling
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Node.java#L767-L779
```
    /**
     Gets the previous Element sibling of this node.

     @return the previous element, or null if there is no previous element
     @see #nextElementSibling()
     */
    public @Nullable Element previousElementSibling() {
        Node prev = this;
        while ((prev = prev.previousSibling()) != null) {
            if (prev instanceof Element) return (Element) prev;
        }
        return null;
    }
```
[ ] jhy--jsoup--retainAll
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/select/Nodes.java#L292-L312
```
    /**
     Retain in this list, and in the DOM, only the nodes that are in the specified collection and are in this list. In
     other words, remove nodes from this list and the DOM any item that is in this list but not in the specified
     collection.

     @param toRemove collection containing nodes to be retained in this list
     @return {@code true} if nodes were removed from this list
     @since 1.17.1
     */
    @Override
    public boolean retainAll(Collection<?> toRemove) {
        boolean anyRemoved = false;
        for (Iterator<T> it = this.iterator(); it.hasNext(); ) {
            T el = it.next();
            if (!toRemove.contains(el)) {
                it.remove();
                anyRemoved = true;
            }
        }
        return anyRemoved;
    }
```
[ ] jhy--jsoup--selectFirst
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/select/Selector.java#L225-L244
```
    /**
     Find the first element matching the query, across multiple roots.

     @param cssQuery CSS selector
     @param roots root elements to descend into
     @return the first matching element, or {@code null} if none
     @since 1.19.1
     */
    public static @Nullable Element selectFirst(String cssQuery, Iterable<Element> roots) {
        Validate.notEmpty(cssQuery);
        Validate.notNull(roots);
        Evaluator evaluator = evaluatorOf(cssQuery);

        for (Element root : roots) {
            Element first = Collector.findFirst(evaluator, root);
            if (first != null) return first;
        }

        return null;
    }
```
[ ] jhy--jsoup--setValue
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Attribute.java#L108-L124
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return Attributes.checkNotNull(oldVal);
    }
```
[ ] jhy--jsoup--siblingNodes
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Node.java#L630-L645
```
    /**
     Retrieves this node's sibling nodes. Similar to {@link #childNodes() node.parent.childNodes()}, but does not
     include this node (a node is not a sibling of itself).
     @return node siblings. If the node has no parent, returns an empty list.
     */
    public List<Node> siblingNodes() {
        if (parentNode == null)
            return Collections.emptyList();

        List<Node> nodes = parentNode.ensureChildNodes();
        List<Node> siblings = new ArrayList<>(nodes.size() - 1);
        for (Node node: nodes)
            if (node != this)
                siblings.add(node);
        return siblings;
    }
```
[ ] jhy--jsoup--sourceRange
https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Attributes.java#L379-L398
```
    /**
     Get the source ranges (start to end position) in the original input source from which this attribute's <b>name</b>
     and <b>value</b> were parsed.
     <p>Position tracking must be enabled prior to parsing the content.</p>
     @param key the attribute name
     @return the ranges for the attribute's name and value, or {@code untracked} if the attribute does not exist or its range
     was not tracked.
     @see org.jsoup.parser.Parser#setTrackPosition(boolean)
     @see Attribute#sourceRange()
     @see Node#sourceRange()
     @see Element#endSourceRange()
     @since 1.17.1
     */
    public Range.AttributeRange sourceRange(String key) {
        if (!hasKey(key)) return UntrackedAttr;
        Map<String, Range.AttributeRange> ranges = getRanges();
        if (ranges == null) return Range.AttributeRange.UntrackedAttr;
        Range.AttributeRange range = ranges.get(key);
        return range != null ? range : Range.AttributeRange.UntrackedAttr;
    }
```
[ ] jitsi--jiwer--collect_error_counts
https://github.com/jitsi/jiwer/blob/c1b0d5e005431f5ce4fa6797f48639a8ccaa5042/./src/jiwer/alignment.py#L229-L263
```
def collect_error_counts(output: Union[WordOutput, CharacterOutput]):
    """
    Retrieve three dictionaries, which count the frequency of how often
    each word or character was substituted, inserted, or deleted.
    The substitution dictionary has, as keys, a 2-tuple (from, to).
    The other two dictionaries have the inserted/deleted words or characters as keys.

    Args:
        output: The processed output of reference and hypothesis pair(s).

    Returns:
        (Tuple[dict, dict, dict]): A three-tuple of dictionaries, in the order substitutions, insertions, deletions.
    """
    substitutions = defaultdict(lambda: 0)
    insertions = defaultdict(lambda: 0)
    deletions = defaultdict(lambda: 0)

    for idx, sentence_chunks in enumerate(output.alignments):
        ref = output.references[idx]
        hyp = output.hypotheses[idx]
        sep = " " if isinstance(output, WordOutput) else ""

        for chunk in sentence_chunks:
            if chunk.type == "insert":
                inserted = sep.join(hyp[chunk.hyp_start_idx : chunk.hyp_end_idx])
                insertions[inserted] += 1
            if chunk.type == "delete":
                deleted = sep.join(ref[chunk.ref_start_idx : chunk.ref_end_idx])
                deletions[deleted] += 1
            if chunk.type == "substitute":
                replaced = sep.join(ref[chunk.ref_start_idx : chunk.ref_end_idx])
                by = sep.join(hyp[chunk.hyp_start_idx : chunk.hyp_end_idx])
                substitutions[(replaced, by)] += 1

    return substitutions, insertions, deletions
```
[ ] jmeter-maven-plugin--jmeter-maven-plugin--addAndOverwriteProperties
https://github.com/jmeter-maven-plugin/jmeter-maven-plugin/blob/13092f3e53c1f9e0f87a81c5b47bc5d814530d55/./src/main/java/com/lazerycode/jmeter/properties/PropertiesFile.java#L93-L107
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
[ ] jmeter-maven-plugin--jmeter-maven-plugin--computeJMeterArgumentsArray
https://github.com/jmeter-maven-plugin/jmeter-maven-plugin/blob/13092f3e53c1f9e0f87a81c5b47bc5d814530d55/./src/main/java/com/lazerycode/jmeter/mojo/AbstractJMeterMojo.java#L245-L272
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
[ ] jmeter-maven-plugin--jmeter-maven-plugin--containsExclusion
https://github.com/jmeter-maven-plugin/jmeter-maven-plugin/blob/13092f3e53c1f9e0f87a81c5b47bc5d814530d55/./src/main/java/com/lazerycode/jmeter/configuration/ArtifactHelpers.java#L100-L122
```
    /**
     * Exclusive can be specified by wildcard:
     * -- groupId:artifactId:*:*
     * -- groupId:*:*:*
     * <p>
     * And in general, to require a strict match up to the version and the classifier is not necessary
     * <p>
     * TODO: the correct fix would be to rewrite {@link Exclusion # equals (Object)}, but what about the boundary case:
     * If contains (id1: *: *: *, id1: id2: *: *) == true, then that's equals ??
     * TODO: there must be useful code in Aether or maven on this topic
     * <p>
     *
     * @param exclusions Collection of exclusions
     * @param exclusion  Specific exclusion to search through collection for
     * @return boolean
     */
    public static boolean containsExclusion(Collection<Exclusion> exclusions, Exclusion exclusion) {
        return Optional.ofNullable(exclusions).orElse(Collections.emptyList())
                .stream().anyMatch(selectedExclusion ->
                        null != exclusion && selectedExclusion.getGroupId().equals(exclusion.getGroupId()) &&
                                (selectedExclusion.getArtifactId().equals(exclusion.getArtifactId()) || (selectedExclusion.getArtifactId().equals(ARTIFACT_STAR)))
                );
    }
```
[ ] joowani--binarytree--_is_symmetric
https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/./binarytree/__init__.py#L1783-L1803
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)
```
[ ] joowani--binarytree--equals
https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/./binarytree/__init__.py#L749-L778
```
    def equals(self, other: "Node") -> bool:
        """Check if this binary tree is equal to other binary tree.

        :param other: Root of the other binary tree.
        :type other: binarytree.Node
        :return: True if the binary trees are equal, False otherwise.
        :rtype: bool
        """
        stack1: List[Optional[Node]] = [self]
        stack2: List[Optional[Node]] = [other]

        while stack1 or stack2:
            node1 = stack1.pop()
            node2 = stack2.pop()

            if node1 is None and node2 is None:
                continue
            elif node1 is None or node2 is None:
                return False
            elif not isinstance(node2, Node):
                return False
            else:
                if node1.val != node2.val:
                    return False
                stack1.append(node1.right)
                stack1.append(node1.left)
                stack2.append(node2.right)
                stack2.append(node2.left)

        return True
```
[ ] joowani--binarytree--get_parent
https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/./binarytree/__init__.py#L2131-L2180
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
[ ] joowani--binarytree--postorder
https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/./binarytree/__init__.py#L1642-L1686
```
    @property
    def postorder(self) -> List["Node"]:
        """Return the nodes in the binary tree using post-order_ traversal.

        A post-order_ traversal visits left subtree, right subtree, then root.

        .. _post-order: https://en.wikipedia.org/wiki/Tree_traversal

        :return: List of nodes.
        :rtype: [binarytree.Node]

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
                __1
               /   \\
              2     3
             / \\
            4   5
            <BLANKLINE>
            >>> root.postorder
            [Node(4), Node(5), Node(2), Node(3), Node(1)]
        """
        result: List[Node] = []
        stack: List[Optional[Node]] = [self]

        while stack:
            node = stack.pop()
            if node:
                result.append(node)
                stack.append(node.left)
                stack.append(node.right)

        return result[::-1]
```
[ ] joowani--binarytree--svg
https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/./binarytree/__init__.py#L521-L588
```
    def svg(self, node_radius: int = 16) -> str:
        """Generate SVG XML.

        :param node_radius: Node radius in pixels (default: 16).
        :type node_radius: int
        :return: Raw SVG XML.
        :rtype: str
        """
        tree_height = self.height
        scale = node_radius * 3
        xml: Deque[str] = deque()

        def scale_x(x: int, y: int) -> float:
            diff = tree_height - y
            x = 2 ** (diff + 1) * x + 2**diff - 1
            return 1 + node_radius + scale * x / 2

        def scale_y(y: int) -> float:
            return scale * (1 + y)

        def add_edge(parent_x: int, parent_y: int, node_x: int, node_y: int) -> None:
            xml.appendleft(
                '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'.format(
                    x1=scale_x(parent_x, parent_y),
                    y1=scale_y(parent_y),
                    x2=scale_x(node_x, node_y),
                    y2=scale_y(node_y),
                )
            )

        def add_node(node_x: int, node_y: int, node_value: NodeValue) -> None:
            x, y = scale_x(node_x, node_y), scale_y(node_y)
            xml.append(f'<circle class="node" cx="{x}" cy="{y}" r="{node_radius}"/>')
            xml.append(f'<text class="value" x="{x}" y="{y}">{node_value}</text>')

        current_nodes = [self.left, self.right]
        has_more_nodes = True
        y = 1

        add_node(0, 0, self.value)

        while has_more_nodes:

            has_more_nodes = False
            next_nodes: List[Optional[Node]] = []

            for x, node in enumerate(current_nodes):
                if node is None:
                    next_nodes.append(None)
                    next_nodes.append(None)
                else:
                    if node.left is not None or node.right is not None:
                        has_more_nodes = True

                    add_edge(x // 2, y - 1, x, y)
                    add_node(x, y, node.value)

                    next_nodes.append(node.left)
                    next_nodes.append(node.right)

            current_nodes = next_nodes
            y += 1

        return _SVG_XML_TEMPLATE.format(
            width=scale * (2**tree_height),
            height=scale * (2 + tree_height),
            body="\n".join(xml),
        )
```
[ ] kellyjonbrazil--jc--_add_text_kv
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/nmcli.py#L232-L244
```
def _add_text_kv(key: str, value: Optional[str]) -> Optional[Dict]:
    """
    Add keys with _text suffix if there is a text description inside
    parenthesis at the end of a value. The value of the _text field will
    only be the text inside the parenthesis. This allows cleanup of the
    original field (convert to int/float/etc) without losing information.
    """
    if value and '(' in value and value.endswith(')'):
        new_val = re.search(r'\((\w+)\)$', value)
        if new_val:
            return ({key + '_text': new_val.group(1)})

    return None
```
[ ] kellyjonbrazil--jc--_bundle_match
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/ifconfig.py#L330-L337
```
def _bundle_match(pattern_list, string):
    """Returns a match object if a string matches one of a list of patterns.
    If no match is found, returns None"""
    for pattern in pattern_list:
        match = re.search(pattern, string)
        if match:
            return match
    return None
```
[ ] kellyjonbrazil--jc--_create_table_dict
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asciitable_m.py#L420-L431
```
def _create_table_dict(header: List[str], data: List[List[str]]) -> List[Dict[str, Optional[str]]]:
    """
    zip the headers and data to create a list of dictionaries. Also convert
    empty strings to None.
    """
    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data]
    for row in table_list_dict:
        for k, v in row.items():
            if v == '':
                row[k] = None

    return table_list_dict
```
[ ] kellyjonbrazil--jc--_entries_for_this_bus_and_interface_idx_exist
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/lsusb.py#L391-L402
```
    def _entries_for_this_bus_and_interface_idx_exist(self, bus_idx, iface_idx):
        """Returns true if there are object entries for the corresponding bus index
        and interface index"""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx \
                and item[keyname]['_state']['interface_descriptor_idx'] == iface_idx:

                return True

        return False
```
[ ] kellyjonbrazil--jc--_get_data
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asciitable_m.py#L349-L374
```
def _get_data(table: Iterable[Tuple[int, List]]) -> List[List[List[str]]]:
    """
    return a list of rows, which are lists made up of lists of strings:
        [                                # data
            [                            # data rows
                ['str', 'str', 'str'],   # data lines
                ['str', 'str', 'str']
            ]
        ]
    """
    result: List[List[List[str]]] = []
    current_row = 1
    this_line: List[List[str]] = []
    for row_num, line in table:
        if row_num != 0:
            if row_num != current_row:
                result.append(this_line)
                current_row = row_num
                this_line = []

            this_line.append(line)

    if this_line:
        result.append(this_line)

    return result
```
[ ] kellyjonbrazil--jc--_get_headers
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asciitable_m.py#L334-L346
```
def _get_headers(table: Iterable[Tuple[int, List]]) -> List[List[str]]:
    """
    return a list of all of the header rows (which are lists of strings.
        [                            # headers
            ['str', 'str', 'str'],   # header rows
            ['str', 'str', 'str']
        ]
    """
    result = []
    for row_num, line in table:
        if row_num == 0:
            result.append(line)
    return result
```
[ ] kellyjonbrazil--jc--_long_filesystem_hash
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/df.py#L174-L197
```
def _long_filesystem_hash(header, line):
    """
    Returns truncated hash and value of the filesystem field if it is too
    long for the column.
    """
    filesystem_field = line.split()[0]

    # get length of filesystem column
    space_count = 0
    for char in header[10:]:
        if char == ' ':
            space_count += 1
            continue

        break

    filesystem_col_len = space_count + 9

    # return the hash and value if the field data is longer than the column length
    if len(filesystem_field) > filesystem_col_len:
        truncated_hash = hashlib.sha256(filesystem_field.encode('utf-8')).hexdigest()[:filesystem_col_len]
        return truncated_hash, filesystem_field

    return None, None
```
[x] kellyjonbrazil--jc--_process-125
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/sysctl.py#L72-L92
```
def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    for key in proc_data:
        try:
            proc_data[key] = int(proc_data[key])
        except (ValueError):
            try:
                proc_data[key] = float(proc_data[key])
            except (ValueError):
                pass
    return proc_data
```
[x] kellyjonbrazil--jc--_process-42
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/iftop.py#L202-L246
```
def _process(proc_data: List[JSONDictType], quiet: bool = False) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    string_to_bytes_fields = ["last_2s", "last_10s", "last_40s", "cumulative"]
    one_nesting = [
        "total_send_rate",
        "total_receive_rate",
        "total_send_and_receive_rate",
        "peak_rate",
        "cumulative_rate",
    ]

    if not proc_data:
        return proc_data
    for entry in proc_data:
        # print(f"{entry=}")
        for entry_key in entry:
            # print(f"{entry_key=}")
            if entry_key in one_nesting:
                # print(f"{entry[entry_key]=}")
                for one_nesting_item_key in entry[entry_key]:
                    # print(f"{one_nesting_item_key=}")
                    if one_nesting_item_key in string_to_bytes_fields:
                        entry[entry_key][one_nesting_item_key] = jc.utils.convert_size_to_int(entry[entry_key][one_nesting_item_key])
            elif entry_key == "clients":
                for client in entry[entry_key]:
                    # print(f"{client=}")
                    if "connections" not in client:
                        continue
                    for connection in client["connections"]:
                        # print(f"{connection=}")
                        for connection_key in connection:
                            # print(f"{connection_key=}")
                            if connection_key in string_to_bytes_fields:
                                connection[connection_key] = jc.utils.convert_size_to_int(connection[connection_key])
    return proc_data
```
[ ] kellyjonbrazil--jc--_update_output
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/lsusb.py#L365-L383
```
    def _update_output(self, bus_idx, output_line):
        """modifies output_line dictionary for the corresponding bus index.
        output_line is the self.output_line attribute from the _lsusb object."""
        for item in self.list:
            keyname = tuple(item.keys())[0]

            if '_state' in item[keyname] and item[keyname]['_state']['bus_idx'] == bus_idx:
                # is this a top level value or an attribute?
                if item[keyname]['_state']['attribute_value']:
                    last_item = item[keyname]['_state']['last_item']
                    if 'attributes' not in output_line[f'{self.name}'][last_item]:
                        output_line[f'{self.name}'][last_item]['attributes'] = []

                    this_attribute = f'{keyname} {item[keyname].get("value", "")} {item[keyname].get("description", "")}'.strip()
                    output_line[f'{self.name}'][last_item]['attributes'].append(this_attribute)
                    continue

                output_line[f'{self.name}'].update(item)
                del output_line[f'{self.name}'][keyname]['_state']
```
[ ] kellyjonbrazil--jc--_urlunquote
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asn1crypto/_iri.py#L224-L270
```
def _urlunquote(byte_string, remap=None, preserve=None):
    """
    Unquotes a URI portion from a byte string into unicode using UTF-8

    :param byte_string:
        A byte string of the data to unquote

    :param remap:
        A list of characters (as unicode) that should be re-mapped to a
        %XX encoding. This is used when characters are not valid in part of a
        URL.

    :param preserve:
        A bool - indicates that the chars to be remapped if they occur in
        non-hex form, should be preserved. E.g. / for URL path.

    :return:
        A unicode string
    """

    if byte_string is None:
        return byte_string

    if byte_string == b'':
        return ''

    if preserve:
        replacements = ['\x1A', '\x1C', '\x1D', '\x1E', '\x1F']
        preserve_unmap = {}
        for char in remap:
            replacement = replacements.pop(0)
            preserve_unmap[replacement] = char
            byte_string = byte_string.replace(char.encode('ascii'), replacement.encode('ascii'))

    byte_string = unquote_to_bytes(byte_string)

    if remap:
        for char in remap:
            byte_string = byte_string.replace(char.encode('ascii'), ('%%%02x' % ord(char)).encode('ascii'))

    output = byte_string.decode('utf-8', 'iriutf8')

    if preserve:
        for replacement, original in preserve_unmap.items():
            output = output.replace(replacement, original)

    return output
```
[ ] kellyjonbrazil--jc--all_parser_info
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/lib.py#L661-L693
```
def all_parser_info(
    documentation: bool = False,
    show_hidden: bool = False,
    show_deprecated: bool = False
) -> List[ParserInfoType]:
    """
    Returns a list of dictionaries that includes metadata for all parser
    modules. By default only non-hidden, non-deprecated parsers are
    returned.

    Parameters:

        documentation:      (boolean)    include parser docstrings if `True`
        show_hidden:        (boolean)    also show parsers marked as hidden
                                         in their info metadata.
        show_deprecated:    (boolean)    also show parsers marked as
                                         deprecated in their info metadata.
    """
    plist: List[str] = []
    for p in parsers:
        parser = get_parser(p)

        if not show_hidden and _parser_is_hidden(parser):
            continue

        if not show_deprecated and _parser_is_deprecated(parser):
            continue

        plist.append(p)

    p_info_list: List[ParserInfoType] = [parser_info(p, documentation=documentation) for p in plist]

    return p_info_list
```
[ ] kellyjonbrazil--jc--dotted
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asn1crypto/core.py#L3118-L3150
```
    @property
    def dotted(self):
        """
        :return:
            A unicode string of the object identifier in dotted notation, thus
            ignoring any mapped value
        """

        if self._dotted is None:
            output = []

            part = 0
            for byte in self.contents:
                part = part * 128
                part += byte & 127
                # Last byte in subidentifier has the eighth bit set to 0
                if byte & 0x80 == 0:
                    if len(output) == 0:
                        if part >= 80:
                            output.append(str(2))
                            output.append(str(part - 80))
                        elif part >= 40:
                            output.append(str(1))
                            output.append(str(part - 40))
                        else:
                            output.append(str(0))
                            output.append(str(part))
                    else:
                        output.append(str(part))
                    part = 0

            self._dotted = '.'.join(output)
        return self._dotted
```
[ ] kellyjonbrazil--jc--normalize_key
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/utils.py#L212-L249
```
def normalize_key(data: str) -> str:
    r"""
    Normalize a key name by shifting to lower-case and converting special
    characters to underscores.

    Special characters are defined as `space` and the following:

        !"#$%&'()*+,-./:;<=>?@[\]^`{|}~

    This is a lossy algorithm. Repeating and trailing underscores are
    removed.

    Parameters:

        data:       (string) Input value

    Returns:

        string
    """
    special = r'''!"#$%&'()*+,-./:;<=>?@[\]^`{|}~ '''
    initial_underscore = False
    data = data.strip().lower()

    for special_char in special:
        data = data.replace(special_char, '_')

    if data.startswith('_'):
        initial_underscore = True

    # swap back to space so split() will compress multiple consecutive down to one
    data = data.strip('_').replace('_', ' ')
    data = '_'.join(data.split())

    if initial_underscore:
        data = '_' + data

    return data
```
[x] kellyjonbrazil--jc--parse-213
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/uptime.py#L145-L186
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
[x] kellyjonbrazil--jc--parse-79
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/lsattr.py#L110-L162
```
def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    output: List = []

    cleandata = list(filter(None, data.splitlines()))

    if not jc.utils.has_data(data):
        return output

    for line in cleandata:
        # -R flag returns the output in the format:
        # Folder:
        #   attributes file_in_folder
        if line.endswith(':'):
            continue

        # lsattr: Operation not supported ....
        if line.startswith(ERROR_PREFIX):
            continue

        line_output: Dict = {}

        # attributes file
        # --------------e----- /etc/passwd
        attributes, file = line.split()
        line_output['file'] = file
        for attribute in list(attributes):
            attribute_key = ATTRIBUTES.get(attribute)
            if attribute_key:
                line_output[attribute_key] = True

        if line_output:
            output.append(line_output)

    return output
```
[ ] kellyjonbrazil--jc--remove_quotes
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/utils.py#L190-L209
```
def remove_quotes(data: str) -> str:
    """
    Remove single or double quotes surrounding a string. If no quotes are
    found then the string is returned unmodified.

    Parameters:

        data:       (string) Input value

    Returns:

        string
    """
    if data.startswith('"') and data.endswith('"'):
        data = data[1:-1]

    elif data.startswith("'") and data.endswith("'"):
        data = data[1:-1]

    return data
```
[ ] kellyjonbrazil--jc--set_custom_colors
https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/cli.py#L132-L177
```
    def set_custom_colors(self) -> None:
        """
        Sets the custom_colors dictionary to be used in Pygments custom style class.

        Grab custom colors from JC_COLORS environment variable. JC_COLORS env
        variable takes 4 comma separated string values and should be in the
        format of:

        JC_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>

        Where colors are: black, red, green, yellow, blue, magenta, cyan, gray,
        brightblack, brightred, brightgreen, brightyellow, brightblue, brightmagenta,
        brightcyan, white, default

        Default colors:
        JC_COLORS=blue,brightblack,magenta,green
        JC_COLORS=default,default,default,default
        """
        if PYGMENTS_INSTALLED:
            input_error = False
            env_colors = os.getenv('JC_COLORS')

            if env_colors:
                color_list = env_colors.split(',')
            else:
                color_list = ['default', 'default', 'default', 'default']

            if len(color_list) != 4:
                input_error = True

            for color in color_list:
                if color != 'default' and color not in PYGMENT_COLOR:
                    input_error = True

            # if there is an issue with the env variable, just set all colors to default and move on
            if input_error:
                utils.warning_message(['Could not parse JC_COLORS environment variable'])
                color_list = ['default', 'default', 'default', 'default']

            # Try the color set in the JC_COLORS env variable first. If it is set to default, then fall back to default colors
            self.custom_colors = {
                Name.Tag: f'bold {PYGMENT_COLOR[color_list[0]]}' if color_list[0] != 'default' else f"bold {PYGMENT_COLOR['blue']}",   # key names
                Keyword: PYGMENT_COLOR[color_list[1]] if color_list[1] != 'default' else PYGMENT_COLOR['brightblack'],                 # true, false, null
                Number: PYGMENT_COLOR[color_list[2]] if color_list[2] != 'default' else PYGMENT_COLOR['magenta'],                      # numbers
                String: PYGMENT_COLOR[color_list[3]] if color_list[3] != 'default' else PYGMENT_COLOR['green']                         # strings
            }
```
[ ] keon--algorithms--_load_byte
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/compression/huffman_coding.py#L87-L102
```
    def _load_byte(self, buff_limit=8) -> bool:
        """
        Load next byte is buffer is less than buff_limit
        :param buff_limit:
        :return: True if there is enough bits in buffer to read
        """
        if len(self.buffer) <= buff_limit:
            byte = self.file.read(1)

            if not byte:
                return False

            i = int.from_bytes(byte, "big")
            self.buffer.extend(list("{0:08b}".format(i)))

        return True
```
[ ] keon--algorithms--all_pairs_shortest_path
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/all_pairs_shortest_path.py#L27-L42
```
def all_pairs_shortest_path(adjacency_matrix):
    """
    Given a matrix of the edge weights between respective nodes, returns a
    matrix containing the shortest distance distance between the two nodes.
    """

    new_array = copy.deepcopy(adjacency_matrix)

    size = len(new_array)
    for k in range(size):
        for i in range(size):
            for j in range(size):
                if new_array[i][j] > new_array[i][k] + new_array[k][j]:
                    new_array[i][j] = new_array[i][k] + new_array[k][j]

    return new_array
```
[ ] keon--algorithms--base_to_int
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/maths/base_conversion.py#L33-L49
```
def base_to_int(str_to_convert, base):
    """
        Note : You can use int() built-in function instead of this.
        :type str_to_convert: str
        :type base: int
        :rtype: int
    """

    digit = {}
    for ind, char in enumerate(string.digits + string.ascii_uppercase):
        digit[char] = ind
    multiplier = 1
    res = 0
    for char in str_to_convert[::-1]:
        res += digit[char] * multiplier
        multiplier *= base
    return res
```
[ ] keon--algorithms--bellman_ford
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/bellman_ford.py#L5-L38
```
def bellman_ford(graph, source):
    """
    This Bellman-Ford Code is for determination whether we can get
    shortest path from given graph or not for single-source shortest-paths problem.
    In other words, if given graph has any negative-weight cycle that is reachable
    from the source, then it will give answer False for "no solution exits".
    For argument graph, it should be a dictionary type
    such as
    graph = {
        'a': {'b': 6, 'e': 7},
        'b': {'c': 5, 'd': -4, 'e': 8},
        'c': {'b': -2},
        'd': {'a': 2, 'c': 7},
        'e': {'b': -3}
    }
    """
    weight = {}
    pre_node = {}

    initialize_single_source(graph, source, weight, pre_node)

    for _ in range(1, len(graph)):
        for node in graph:
            for adjacent in graph[node]:
                if weight[adjacent] > weight[node] + graph[node][adjacent]:
                    weight[adjacent] = weight[node] + graph[node][adjacent]
                    pre_node[adjacent] = node

    for node in graph:
        for adjacent in graph[node]:
            if weight[adjacent] > weight[node] + graph[node][adjacent]:
                return False

    return True
```
[ ] keon--algorithms--bitonic_sort
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/sort/bitonic_sort.py#L1-L43
```
def bitonic_sort(arr, reverse=False):
    """
    bitonic sort is sorting algorithm to use multiple process, but this code not containing parallel process
    It can sort only array that sizes power of 2
    It can sort array in both increasing order and decreasing order by giving argument true(increasing) and false(decreasing)
    
    Worst-case in parallel: O(log(n)^2)
    Worst-case in non-parallel: O(nlog(n)^2)
    
    reference: https://en.wikipedia.org/wiki/Bitonic_sorter
    """
    def compare(arr, reverse):
        n = len(arr)//2
        for i in range(n):
            if reverse != (arr[i] > arr[i+n]):
                arr[i], arr[i+n] = arr[i+n], arr[i]
        return arr

    def bitonic_merge(arr, reverse):
        n = len(arr)
        
        if n <= 1:
            return arr
        
        arr = compare(arr, reverse)
        left = bitonic_merge(arr[:n // 2], reverse)
        right = bitonic_merge(arr[n // 2:], reverse)
        return left + right
    
    #end of function(compare and bitionic_merge) definition
    n = len(arr)
    if n <= 1:
        return arr
    # checks if n is power of two
    if not (n and (not(n & (n - 1))) ):
        raise ValueError("the size of input should be power of two")
    
    left = bitonic_sort(arr[:n // 2], True)
    right = bitonic_sort(arr[n // 2:], False)

    arr = bitonic_merge(left + right, reverse)
        
    return arr
```
[ ] keon--algorithms--check_bipartite
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/check_bipartite.py#L6-L40
```
def check_bipartite(adj_list):
    """
    Determine if the given graph is bipartite.

    Time complexity is O(|E|)
    Space complexity is O(|V|)
    """

    vertices = len(adj_list)

    # Divide vertexes in the graph into set_type 0 and 1
    # Initialize all set_types as -1
    set_type = [-1 for v in range(vertices)]
    set_type[0] = 0

    queue = [0]

    while queue:
        current = queue.pop(0)

        # If there is a self-loop, it cannot be bipartite
        if adj_list[current][current]:
            return False

        for adjacent in range(vertices):
            if adj_list[current][adjacent]:
                if set_type[adjacent] == set_type[current]:
                    return False

                if set_type[adjacent] == -1:
                    # set type of u opposite of v
                    set_type[adjacent] = 1 - set_type[current]
                    queue.append(adjacent)

    return True
```
[ ] keon--algorithms--cholesky_decomposition
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/matrix/cholesky_matrix_decomposition.py#L27-L51
```
def cholesky_decomposition(A):
    """
    :param A: Hermitian positive-definite matrix of type List[List[float]]
    :return: matrix of type List[List[float]] if A can be decomposed,
    otherwise None
    """
    n = len(A)
    for ai in A:
        if len(ai) != n:
            return None
    V = [[0.0] * n for _ in range(n)]
    for j in range(n):
        sum_diagonal_element = 0
        for k in range(j):
            sum_diagonal_element = sum_diagonal_element + math.pow(V[j][k], 2)
        sum_diagonal_element = A[j][j] - sum_diagonal_element
        if sum_diagonal_element <= 0:
            return None
        V[j][j] = math.pow(sum_diagonal_element, 0.5)
        for i in range(j+1, n):
            sum_other_element = 0
            for k in range(j):
                sum_other_element += V[i][k]*V[j][k]
            V[i][j] = (A[i][j] - sum_other_element)/V[j][j]
    return V
```
[ ] keon--algorithms--combination_sum_bottom_up
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/dp/combination_sum.py#L61-L74
```
def combination_sum_bottom_up(nums, target):
    """Find number of possible combinations in nums that add up to target, in bottom-up manner.

    Keyword arguments:
    nums -- positive integer array without duplicates
    target -- integer describing what a valid combination should add to
    """
    combs = [0] * (target + 1)
    combs[0] = 1
    for i in range(0, len(combs)):
        for num in nums:
            if i - num >= 0:
                combs[i] += combs[i - num]
    return combs[target]
```
[ ] keon--algorithms--contains_cycle
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/cycle_detection.py#L38-L55
```
def contains_cycle(graph):
    """
    Determines if there is a cycle in the given graph.
    The graph should be given as a dictionary:

        graph = {'A': ['B', 'C'],
                 'B': ['D'],
                 'C': ['F'],
                 'D': ['E', 'F'],
                 'E': ['B'],
                 'F': []}
    """
    traversal_states = {vertex: TraversalState.WHITE for vertex in graph}
    for vertex, state in traversal_states.items():
        if (state == TraversalState.WHITE and
           is_in_cycle(graph, traversal_states, vertex)):
            return True
    return False
```
[ ] keon--algorithms--count
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/dp/coin_change.py#L19-L34
```
def count(coins, value):
    """ Find number of combination of `coins` that adds upp to `value`

    Keyword arguments:
    coins -- int[]
    value -- int
    """
    # initialize dp array and set base case as 1
    dp_array = [1] + [0] * value

    # fill dp in a bottom up manner
    for coin in coins:
        for i in range(coin, value+1):
            dp_array[i] += dp_array[i-coin]

    return dp_array[value]
```
[ ] keon--algorithms--decode_rle
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/compression/rle_compression.py#L39-L58
```
def decode_rle(input):
    """
    Gets a stream of data and decompresses it
    under a Run-Length Decoding.
    :param input: The data to be decoded.
    :return: The decoded string.
    """
    decode_str = ''
    count = ''

    for ch in input:
        # If not numerical
        if not ch.isdigit():
            # Expand it for the decoding
            decode_str += ch * int(count)
            count = ''
        else:
            # Add it in the counter
            count += ch
    return decode_str
```
[ ] keon--algorithms--distance
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/ml/nearest_neighbor.py#L3-L19
```
def distance(x,y):
    """[summary]
    HELPER-FUNCTION
    calculates the (eulidean) distance between vector x and y.

    Arguments:
        x {[tuple]} -- [vector]
        y {[tuple]} -- [vector]
    """
    assert len(x) == len(y), "The vector must have same length"
    result = ()
    sum = 0
    for i in range(len(x)):
        result += (x[i] -y[i],)
    for component in result:
        sum += component**2
    return math.sqrt(sum)
```
[ ] keon--algorithms--find_k_factor
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/dp/k_factor.py#L33-L85
```
def find_k_factor(length, k_factor):
    """Find the number of strings of length `length` with K factor = `k_factor`.

    Keyword arguments:
    length -- integer
    k_factor -- integer
    """
    mat=[[[0 for i in range(4)]for j in range((length-1)//3+2)]for k in range(length+1)]
    if 3*k_factor+1>length:
        return 0
    #base cases
    mat[1][0][0]=1
    mat[1][0][1]=0
    mat[1][0][2]=0
    mat[1][0][3]=25

    for i in range(2,length+1):
        for j in range((length-1)//3+2):
            if j==0:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1<i:
                #adding a at the end
                mat[i][j][0]=mat[i-1][j][0]+mat[i-1][j][1]+mat[i-1][j][3]+mat[i-1][j-1][2]

                #adding b at the end
                mat[i][j][1]=mat[i-1][j][0]
                mat[i][j][2]=mat[i-1][j][1]

                #adding any other lowercase character
                mat[i][j][3]=mat[i-1][j][0]*24+mat[i-1][j][1]*24+mat[i-1][j][2]*25+mat[i-1][j][3]*25

            elif 3*j+1==i:
                mat[i][j][0]=1
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

            else:
                mat[i][j][0]=0
                mat[i][j][1]=0
                mat[i][j][2]=0
                mat[i][j][3]=0

    return sum(mat[length][k_factor])
```
[ ] keon--algorithms--first_occurrence
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/search/first_occurrence.py#L6-L23
```
def first_occurrence(array, query):
    """
    Returns the index of the first occurance of the given element in an array.
    The array has to be sorted in increasing order.
    """

    low, high = 0, len(array) - 1
    while low <= high:
        mid = low + (high-low)//2 #Now mid will be ininteger range
        #print("lo: ", lo, " hi: ", hi, " mid: ", mid)
        if low == high:
            break
        if array[mid] < query:
            low = mid + 1
        else:
            high = mid
    if array[low] == query:
        return low
```
[ ] keon--algorithms--get_factors_iterative1
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/dfs/all_factors.py#L63-L84
```
def get_factors_iterative1(n):
    """[summary]
    Computes all factors of n.
    Translated the function get_factors(...) in
    a call-stack modell.

    Arguments:
        n {[int]} -- [to analysed number]
    
    Returns:
        [list of lists] -- [all factors]
    """

    todo, res = [(n, 2, [])], []
    while todo:
        n, i, combi = todo.pop()
        while i * i <= n:
            if n % i == 0:
                res += combi + [i, n//i],
                todo.append((n//i, i, combi+[i])),
            i += 1
    return res
```
[ ] keon--algorithms--get_longest_non_repeat_v2
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/arrays/longest_non_repeat.py#L71-L91
```
def get_longest_non_repeat_v2(string):
    """
    Find the length of the longest substring
    without repeating characters.
    Uses alternative algorithm.
    Return max_len and the substring as a tuple
    """
    if string is None:
        return 0, ''
    sub_string = ''
    start, max_len = 0, 0
    used_char = {}
    for index, char in enumerate(string):
        if char in used_char and start <= used_char[char]:
            start = used_char[char] + 1
        else:
            if index - start + 1 > max_len:
                max_len = index - start + 1
                sub_string = string[start: index + 1]
        used_char[char] = index
    return max_len, sub_string
```
[ ] keon--algorithms--hailstone
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/maths/hailstone.py#L8-L21
```
def hailstone(n):
    """
    Return the 'hailstone sequence' from n to 1
    n: The starting point of the hailstone sequence
    """

    sequence = [n]
    while n > 1:
        if n%2 != 0:
            n = 3*n + 1
        else:
            n = int(n/2)
        sequence.append(n)
    return sequence
```
[ ] keon--algorithms--is_palindrome_dict
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/linkedlist/is_palindrome.py#L52-L89
```
def is_palindrome_dict(head):
    """
    This function builds up a dictionary where the keys are the values of the list,
    and the values are the positions at which these values occur in the list.
    We then iterate over the dict and if there is more than one key with an odd
    number of occurrences, bail out and return False.
    Otherwise, we want to ensure that the positions of occurrence sum to the
    value of the length of the list - 1, working from the outside of the list inward.
    For example:
    Input: 1 -> 1 -> 2 -> 3 -> 2 -> 1 -> 1
    d = {1: [0,1,5,6], 2: [2,4], 3: [3]}
    '3' is the middle outlier, 2+4=6, 0+6=6 and 5+1=6 so we have a palindrome.
    """
    if not head or not head.next:
        return True
    d = {}
    pos = 0
    while head:
        if head.val in d.keys():
            d[head.val].append(pos)
        else:
            d[head.val] = [pos]
        head = head.next
        pos += 1
    checksum = pos - 1
    middle = 0
    for v in d.values():
        if len(v) % 2 != 0:
            middle += 1
        else:
            step = 0
            for i in range(0, len(v)):
                if v[i] + v[len(v) - 1 - step] != checksum:
                    return False
                step += 1
        if middle > 1:
            return False
    return True
```
[ ] keon--algorithms--k_closest
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/heap/k_closest_points.py#L15-L43
```
def k_closest(points, k, origin=(0, 0)):
    # Time: O(k+(n-k)logk)
    # Space: O(k)
    """Initialize max heap with first k points.
    Python does not support a max heap; thus we can use the default min heap
    where the keys (distance) are negated.
    """
    heap = [(-distance(p, origin), p) for p in points[:k]]
    heapify(heap)

    """
    For every point p in points[k:],
    check if p is smaller than the root of the max heap;
    if it is, add p to heap and remove root. Reheapify.
    """
    for point in points[k:]:
        dist = distance(point, origin)

        heappushpop(heap, (-dist, point))  # heappushpop does conditional check
        """Same as:
            if d < -heap[0][0]:
                heappush(heap, (-d,p))
                heappop(heap)

        Note: heappushpop is more efficient than separate push and pop calls.
        Each heappushpop call takes O(logk) time.
        """

    return [point for nd, point in heap]  # return points in heap
```
[ ] keon--algorithms--longest_increasing_subsequence
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/dp/longest_increasing.py#L24-L38
```
def longest_increasing_subsequence(sequence):
    """
    Dynamic Programming Algorithm for
    counting the length of longest increasing subsequence
    type sequence: list[int]
    rtype: int
    """
    length = len(sequence)
    counts = [1 for _ in range(length)]
    for i in range(1, length):
        for j in range(0, i):
            if sequence[i] > sequence[j]:
                counts[i] = max(counts[i], counts[j] + 1)
                print(counts)
    return max(counts)
```
[ ] keon--algorithms--matrix_exponentiation
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/matrix/matrix_exponentiation.py#L30-L43
```
def matrix_exponentiation(mat: list, n: int) -> list:
    """
    Calculates mat^n by repeated squaring
    Time Complexity: O(d^3 log(n))
                     d: dimension of the square matrix mat
                     n: power the matrix is raised to
    """
    if n == 0:
        return identity(len(mat))
    elif n % 2 == 1:
        return multiply(matrix_exponentiation(mat, n - 1), mat)
    else:
        tmp = matrix_exponentiation(mat, n // 2)
        return multiply(tmp, tmp)
```
[ ] keon--algorithms--n_sum
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/arrays/n_sum.py#L34-L140
```
def n_sum(n, nums, target, **kv):
    """
    n: int
    nums: list[object]
    target: object
    sum_closure: function, optional
        Given two elements of nums, return sum of both.
    compare_closure: function, optional
        Given one object of nums and target, return -1, 1, or 0.
    same_closure: function, optional
        Given two object of nums, return bool.
    return: list[list[object]]

    Note:
    1. type of sum_closure's return should be same 
       as type of compare_closure's first param
    """

    def sum_closure_default(a, b):
        return a + b

    def compare_closure_default(num, target):
        """ above, below, or right on? """
        if num < target:
            return -1
        elif num > target:
            return 1
        else:
            return 0

    def same_closure_default(a, b):
        return a == b

    def n_sum(n, nums, target):
        if n == 2:      # want answers with only 2 terms? easy!
            results = two_sum(nums, target)
        else:
            results = []
            prev_num = None
            for index, num in enumerate(nums):
                if prev_num is not None and \
                   same_closure(prev_num, num):
                    continue

                prev_num = num
                n_minus1_results = (
                    n_sum(                      # recursive call
                        n - 1,                  # a
                        nums[index + 1:],       # b
                        target - num            # c
                        )   # x = n_sum( a, b, c )
                    )   # n_minus1_results = x

                n_minus1_results = (
                    append_elem_to_each_list(num, n_minus1_results)
                    )
                results += n_minus1_results
        return union(results)

    def two_sum(nums, target):
        nums.sort()
        lt = 0
        rt = len(nums) - 1
        results = []
        while lt < rt:
            sum_ = sum_closure(nums[lt], nums[rt])
            flag = compare_closure(sum_, target)
            if flag == -1:
                lt += 1
            elif flag == 1:
                rt -= 1
            else:
                results.append(sorted([nums[lt], nums[rt]]))
                lt += 1
                rt -= 1
                while (lt < len(nums) and
                       same_closure(nums[lt - 1], nums[lt])):
                    lt += 1
                while (0 <= rt and
                       same_closure(nums[rt], nums[rt + 1])):
                    rt -= 1
        return results

    def append_elem_to_each_list(elem, container):
        results = []
        for elems in container:
            elems.append(elem)
            results.append(sorted(elems))
        return results

    def union(duplicate_results):
        results = []

        if len(duplicate_results) != 0:
            duplicate_results.sort()
            results.append(duplicate_results[0])
            for result in duplicate_results[1:]:
                if results[-1] != result:
                    results.append(result)

        return results

    sum_closure = kv.get('sum_closure', sum_closure_default)
    same_closure = kv.get('same_closure', same_closure_default)
    compare_closure = kv.get('compare_closure', compare_closure_default)
    nums.sort()
    return n_sum(n, nums, target)
```
[ ] keon--algorithms--num_perfect_squares
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/maths/num_perfect_squares.py#L17-L47
```
def num_perfect_squares(number):
    """
    Returns the smallest number of perfect squares that sum to the specified number.
    :return: int between 1 - 4
    """
    # If the number is a perfect square then we only need 1 number.
    if int(math.sqrt(number))**2 == number:
        return 1

    # We check if https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem holds and divide
    # the number accordingly. Ie. if the number can be written as a sum of 3 squares (where the
    # 0^2 is allowed), which is possible for all numbers except those of the form: 4^a(8b + 7).
    while number > 0 and number % 4 == 0:
        number /= 4

    # If the number is of the form: 4^a(8b + 7) it can't be expressed as a sum of three (or less
    # excluding the 0^2) perfect squares. If the number was of that form, the previous while loop
    # divided away the 4^a, so by now it would be of the form: 8b + 7. So check if this is the case
    # and return 4 since it neccessarily must be a sum of 4 perfect squares, in accordance 
    # with https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem.
    if number % 8 == 7:
        return 4

    # By now we know that the number wasn't of the form 4^a(8b + 7) so it can be expressed as a sum
    # of 3 or less perfect squares. Try first to express it as a sum of 2 perfect squares, and if
    # that fails, we know finally that it can be expressed as a sum of 3 perfect squares.
    for i in range(1, int(math.sqrt(number)) + 1):
        if int(math.sqrt(number - i**2))**2 == number - i**2:
            return 2

    return 3
```
[ ] keon--algorithms--pancake_sort
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/sort/pancake_sort.py#L1-L25
```
def pancake_sort(arr):
    """
    Pancake_sort
    Sorting a given array
    mutation of selection sort

    reference: https://www.geeksforgeeks.org/pancake-sorting/
    
    Overall time complexity : O(N^2)
    """

    len_arr = len(arr)
    if len_arr <= 1:
        return arr
    for cur in range(len(arr), 1, -1):
        #Finding index of maximum number in arr
        index_max = arr.index(max(arr[0:cur]))
        if index_max+1 != cur:
            #Needs moving
            if index_max != 0:
                #reverse from 0 to index_max
                arr[:index_max+1] = reversed(arr[:index_max+1])
            # Reverse list
            arr[:cur] = reversed(arr[:cur])
    return arr
```
[ ] keon--algorithms--power_recur
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/maths/power.py#L27-L48
```
def power_recur(a: int, n: int, mod: int = None):
    """
    Recursive version of binary exponentiation

    Calculate a ^ n
    if mod is specified, return the result modulo mod

    Time Complexity :  O(log(n))
    Space Complexity : O(log(n))
    """
    if n == 0:
        ans = 1
    elif n == 1:
        ans = a
    else:
        ans = power_recur(a, n // 2, mod)
        ans = ans * ans
        if n % 2:
            ans = ans * a
    if mod:
        ans %= mod
    return ans
```
[ ] keon--algorithms--push
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/queues/priority_queue.py#L38-L49
```
    def push(self, item, priority=None):
        """Push the item in the priority queue.
        if priority is not given, priority is set to the value of item.
        """
        priority = item if priority is None else priority
        node = PriorityQueueNode(item, priority)
        for index, current in enumerate(self.priority_queue_list):
            if current.priority < node.priority:
                self.priority_queue_list.insert(index, node)
                return
        # when traversed complete queue
        self.priority_queue_list.append(node)
```
[x] keon--algorithms--rotate_v1
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/arrays/rotate.py#L13-L29
```
def rotate_v1(array, k):
    """
    Rotate the entire array 'k' times
    T(n)- O(nk)

    :type array: List[int]
    :type k: int
    :rtype: void Do not return anything, modify array in-place instead.
    """
    array = array[:]
    n = len(array)
    for i in range(k):      # unused variable is not a problem
        temp = array[n - 1]
        for j in range(n-1, 0, -1):
            array[j] = array[j - 1]
        array[0] = temp
    return array
```
[ ] keon--algorithms--search_insert
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/search/search_insert.py#L5-L24
```
def search_insert(array, val):
    """
    Given a sorted array and a target value, return the index if the target is
    found. If not, return the index where it would be if it were inserted in order.

    For example:
    [1,3,5,6], 5 -> 2
    [1,3,5,6], 2 -> 1
    [1,3,5,6], 7 -> 4
    [1,3,5,6], 0 -> 0
    """
    low = 0
    high = len(array) - 1
    while low <=  high:
        mid = low + (high - low) // 2
        if val > array[mid]:
            low = mid + 1
        else:
            high = mid - 1
    return low
```
[ ] keon--algorithms--search_rotate
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/search/search_rotate.py#L39-L61
```
def search_rotate(array, val):
    """
    Finds the index of the given value in an array that has been sorted in
    ascending order and then rotated at some unknown pivot.
    """
    low, high = 0, len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        if val == array[mid]:
            return mid

        if array[low] <= array[mid]:
            if array[low] <= val <= array[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if array[mid] <= val <= array[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1
```
[ ] keon--algorithms--solve_chinese_remainder
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/maths/chinese_remainder_theorem.py#L7-L39
```
def solve_chinese_remainder(nums : List[int], rems : List[int]):
    """
    Computes the smallest x that satisfies the chinese remainder theorem
    for a system of equations.
    The system of equations has the form:
    x % nums[0] = rems[0]
    x % nums[1] = rems[1]
    ...
    x % nums[k - 1] = rems[k - 1]
    Where k is the number of elements in nums and rems, k > 0.
    All numbers in nums needs to be pariwise coprime otherwise an exception is raised
    returns x: the smallest value for x that satisfies the system of equations
    """
    if not len(nums) == len(rems):
        raise Exception("nums and rems should have equal length")
    if not len(nums) > 0:
        raise Exception("Lists nums and rems need to contain at least one element")
    for num in nums:
        if not num > 1:
            raise Exception("All numbers in nums needs to be > 1")
    if not _check_coprime(nums):
        raise Exception("All pairs of numbers in nums are not coprime")
    k = len(nums)
    x = 1
    while True:
        i = 0
        while i < k:
            if x % nums[i] != rems[i]:
                break
            i += 1
        if i == k:
            return x
        x += 1
```
[ ] keon--algorithms--strongconnect
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/tarjan.py#L29-L65
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
[x] keon--algorithms--ternary_search
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/search/ternary_search.py#L14-L42
```
def ternary_search(left, right, key, arr):
    """
    Find the given value (key) in an array sorted in ascending order.
    Returns the index of the value if found, and -1 otherwise.
    If the index is not in the range left..right (ie. left <= index < right) returns -1.
    """

    while right >= left:
        mid1 = left + (right-left) // 3
        mid2 = right - (right-left) // 3

        if key == arr[mid1]:
            return mid1
        if key == mid2:
            return mid2

        if key < arr[mid1]:
            # key lies between l and mid1
            right = mid1 - 1
        elif key > arr[mid2]:
            # key lies between mid2 and r
            left = mid2 + 1
        else:
            # key lies between mid1 and mid2
            left = mid1 + 1
            right = mid2 - 1

    # key not found
    return -1
```
[ ] keon--algorithms--unique_array_sum_combinations
https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/backtrack/array_sum_combinations.py#L59-L84
```
def unique_array_sum_combinations(A, B, C, target):
    """
    1. Sort all the arrays - a,b,c. - This improves average time complexity.
    2. If c[i] < Sum, then look for Sum - c[i] in array a and b.
       When pair found, insert c[i], a[j] & b[k] into the result list.
       This can be done in O(n).
    3. Keep on doing the above procedure while going through complete c array.

    Complexity: O(n(m+p))
    """
    def check_sum(n, *nums):
        if sum(x for x in nums) == n:
            return (True, nums)
        else:
            return (False, nums)

    pro = itertools.product(A, B, C)
    func = partial(check_sum, target)
    sums = list(itertools.starmap(func, pro))

    res = set()
    for s in sums:
        if s[0] is True and s[1] not in res:
            res.add(s[1])

    return list(res)
```
[ ] lark-parser--lark--_add_repeat_opt_rule
https://github.com/lark-parser/lark/blob/f79772cd4c6d2076b5dc01f399dbb816cc484f77/./lark/load_grammar.py#L278-L313
```
    def _add_repeat_opt_rule(self, a, b, target, target_opt, atom):
        """Creates a rule that matches atom 0 to (a*n+b)-1 times.

        When target matches n times atom, and target_opt 0 to n-1 times target_opt,

        First we generate target * i followed by target_opt, for i from 0 to a-1
        These match 0 to n*a - 1 times atom

        Then we generate target * a followed by atom * i, for i from 0 to b-1
        These match n*a to n*a + b-1 times atom

        The created rule will not have any shift/reduce conflicts so that it can be used with lalr

        Example rule when a=3, b=4:

            new_rule: target_opt
                    | target target_opt
                    | target target target_opt

                    | target target target
                    | target target target atom
                    | target target target atom atom
                    | target target target atom atom atom

        """
        key = (a, b, target, atom, "opt")
        try:
            return self.rules_cache[key]
        except KeyError:
            new_name = self._name_rule('repeat_a%d_b%d_opt' % (a, b))
            tree = ST('expansions', [
                ST('expansion', [target]*i + [target_opt]) for i in range(a)
            ] + [
                ST('expansion', [target]*a + [atom]*i) for i in range(b)
            ])
            return self._add_rule(key, new_name, tree)
```
[ ] lark-parser--lark--small_factors
https://github.com/lark-parser/lark/blob/f79772cd4c6d2076b5dc01f399dbb816cc484f77/./lark/utils.py#L365-L386
```
def small_factors(n: int, max_factor: int) -> List[Tuple[int, int]]:
    """
    Splits n up into smaller factors and summands <= max_factor.
    Returns a list of [(a, b), ...]
    so that the following code returns n:

    n = 1
    for a, b in values:
        n = n * a + b

    Currently, we also keep a + b <= max_factor, but that might change
    """
    assert n >= 0
    assert max_factor > 2
    if n <= max_factor:
        return [(n, 0)]

    for a in range(max_factor, 1, -1):
        r, b = divmod(n, a)
        if a + b <= max_factor:
            return small_factors(r, max_factor) + [(a, b)]
    assert False, "Failed to factorize %s" % n
```
[ ] lemire--javaewah--composeToContainer-2
https://github.com/lemire/javaewah/blob/86f37ab370b74282989e40917b2786ad9fb65f94/./src/main/java/com/googlecode/javaewah32/EWAHCompressedBitmap32.java#L1850-L1889
```
    /**
     * Computes a new compressed bitmap containing the composition of
     * the current bitmap with some other bitmap.
     *
     * The composition A.compose(B) is defined as follows: we retain
     * the ith set bit of A only if the ith bit of B is set. For example, 
     * if you have the following bitmap A = { 0, 1, 0, 1, 1, 0 } and want
     * to keep only the second and third ones, you can call A.compose(B) 
     * with B = { 0, 1, 1 } and you will get C = { 0, 0, 0, 1, 1, 0 }.
     *
     *
     * The current bitmap is not modified.
     *
     * The content of the container is overwritten.
     *
     * @param a         the other bitmap (it will not be modified)
     * @param container where we store the result
     */
    public void composeToContainer(final EWAHCompressedBitmap32 a,
                                   final EWAHCompressedBitmap32 container) {
        container.clear();
        final ChunkIterator iterator = chunkIterator();
        final ChunkIterator aIterator = a.chunkIterator();
        int index = 0;
        while(iterator.hasNext() && aIterator.hasNext()) {
            if(!iterator.nextBit()) {
                int length = iterator.nextLength();
                index += length;
                container.setSizeInBits(index, false);
                iterator.move(length);
            } else {
                int length = Math.min(iterator.nextLength(), aIterator.nextLength());
                index += length;
                container.setSizeInBits(index, aIterator.nextBit());
                iterator.move(length);
                aIterator.move(length);
            }
        }
        container.setSizeInBits(sizeInBits, false);
    }
```
[x] lemire--javaewah--nextSetBit
https://github.com/lemire/javaewah/blob/86f37ab370b74282989e40917b2786ad9fb65f94/./src/main/java/com/googlecode/javaewah/datastructure/BitSet.java#L312-L337
```
    /**
     * Usage: for(int i=bs.nextSetBit(0); i&gt;=0; i=bs.nextSetBit(i+1)) {
     * operate on index i here }
     *
     * @param i current set bit
     * @return next set bit or -1
     */
    public int nextSetBit(final int i) {
        int x = i / 64;
        if (x >= this.getNumberOfWords())
            return -1;
        long w = this.data[x];
        w >>>= i;
        if (w != 0) {
            return i + Long.numberOfTrailingZeros(w);
        }
        ++x;
        for (; x < this.getNumberOfWords(); ++x) {
            if (this.data[x] != 0) {
                return x
                        * 64
                        + Long.numberOfTrailingZeros(this.data[x]);
            }
        }
        return -1;
    }
```
[ ] liiight--notifiers--file_list_for_request
https://github.com/liiight/notifiers/blob/351c048eb1d8fefae7d638cf1ac667a69815c79a/./notifiers/utils/requests.py#L84-L95
```
def file_list_for_request(list_of_paths: list, key_name: str, mimetype: str | None = None) -> list:
    """
    Convenience function to construct a list of files for multiple files upload by :mod:`requests`

    :param list_of_paths: Lists of strings to include in files. Should be pre validated for correctness
    :param key_name: The key name to use for the file list in the request
    :param mimetype: If specified, will be included in the requests
    :return: List of open files ready to be used in a request
    """
    if mimetype:
        return [(key_name, (file, open(file, mode="rb"), mimetype)) for file in list_of_paths]
    return [(key_name, (file, open(file, mode="rb"))) for file in list_of_paths]
```
[ ] liiight--notifiers--handle_oneof
https://github.com/liiight/notifiers/blob/351c048eb1d8fefae7d638cf1ac667a69815c79a/./notifiers_cli/utils/dynamic_click.py#L25-L47
```
def handle_oneof(oneof_schema: list) -> tuple:
    """
    Custom handle of `oneOf` JSON schema validator. Tried to match primitive type and see if it should be allowed
     to be passed multiple timns into a command

    :param oneof_schema: `oneOf` JSON schema
    :return: Tuple of :class:`click.ParamType`, ``multiple`` flag and ``description`` of option
    """
    oneof_dict = {schema["type"]: schema for schema in oneof_schema}
    click_type = None
    multiple = False
    description = None
    for key, value in oneof_dict.items():
        if key == "array":
            continue
        if key in SCHEMA_BASE_MAP:
            if oneof_dict.get("array") and oneof_dict["array"]["items"]["type"] == key:
                multiple = True
            # Found a match to a primitive type
            click_type = SCHEMA_BASE_MAP[key]
            description = value.get("title")
            break
    return click_type, multiple, description
```
[ ] liiight--notifiers--merge_dicts
https://github.com/liiight/notifiers/blob/351c048eb1d8fefae7d638cf1ac667a69815c79a/./notifiers/utils/helpers.py#L20-L33
```
def merge_dicts(target_dict: dict, merge_dict: dict) -> dict:
    """
    Merges ``merge_dict`` into ``target_dict`` if the latter does not already contain a value for each of the key
    names in ``merge_dict``. Used to cleanly merge default and environ data into notification payload.

    :param target_dict: The target dict to merge into and return, the user provided data for example
    :param merge_dict: The data that should be merged into the target data
    :return: A dict of merged data
    """
    log.debug("merging dict %s into %s", merge_dict, target_dict)
    for key, value in merge_dict.items():
        if key not in target_dict:
            target_dict[key] = value
    return target_dict
```
[ ] litl--backoff--fibo
https://github.com/litl/backoff/blob/d82b23c42d7a7e2402903e71e7a7f03014a00076/./backoff/_wait_gen.py#L64-L82
```
def fibo(max_value: Optional[int] = None) -> Generator[int, None, None]:
    """Generator for fibonaccial decay.

    Args:
        max_value: The maximum value to yield. Once the value in the
             true fibonacci sequence exceeds this, the value
             of max_value will forever after be yielded.
    """
    # Advance past initial .send() call
    yield  # type: ignore[misc]

    a = 1
    b = 1
    while True:
        if max_value is None or a < max_value:
            yield a
            a, b = b, a + b
        else:
            yield max_value
```
[ ] lmdbjava--lmdbjava--iteratorOp
https://github.com/lmdbjava/lmdbjava/blob/a15f4a71745c4f54961210fe4b939de462b464c1/./src/main/java/org/lmdbjava/KeyRangeType.java#L317-L392
```
  /**
   * Determine the iterator's response to the presented key.
   *
   * @param <T> buffer type
   * @param <C> comparator for the buffers
   * @param start start buffer
   * @param stop stop buffer
   * @param buffer current key returned by LMDB (may be null)
   * @param c comparator (required)
   * @return response to this key
   */
  <T, C extends Comparator<T>> IteratorOp iteratorOp(
      final T start, final T stop, final T buffer, final C c) {
    requireNonNull(c, "Comparator required");
    if (buffer == null) {
      return TERMINATE;
    }
    switch (this) {
      case FORWARD_ALL:
        return RELEASE;
      case FORWARD_AT_LEAST:
        return RELEASE;
      case FORWARD_AT_MOST:
        return c.compare(buffer, stop) > 0 ? TERMINATE : RELEASE;
      case FORWARD_CLOSED:
        return c.compare(buffer, stop) > 0 ? TERMINATE : RELEASE;
      case FORWARD_CLOSED_OPEN:
        return c.compare(buffer, stop) >= 0 ? TERMINATE : RELEASE;
      case FORWARD_GREATER_THAN:
        return c.compare(buffer, start) == 0 ? CALL_NEXT_OP : RELEASE;
      case FORWARD_LESS_THAN:
        return c.compare(buffer, stop) >= 0 ? TERMINATE : RELEASE;
      case FORWARD_OPEN:
        if (c.compare(buffer, start) == 0) {
          return CALL_NEXT_OP;
        }
        return c.compare(buffer, stop) >= 0 ? TERMINATE : RELEASE;
      case FORWARD_OPEN_CLOSED:
        if (c.compare(buffer, start) == 0) {
          return CALL_NEXT_OP;
        }
        return c.compare(buffer, stop) > 0 ? TERMINATE : RELEASE;
      case BACKWARD_ALL:
        return RELEASE;
      case BACKWARD_AT_LEAST:
        return c.compare(buffer, start) > 0 ? CALL_NEXT_OP : RELEASE; // rewind
      case BACKWARD_AT_MOST:
        return c.compare(buffer, stop) >= 0 ? RELEASE : TERMINATE;
      case BACKWARD_CLOSED:
        if (c.compare(buffer, start) > 0) {
          return CALL_NEXT_OP; // rewind
        }
        return c.compare(buffer, stop) >= 0 ? RELEASE : TERMINATE;
      case BACKWARD_CLOSED_OPEN:
        if (c.compare(buffer, start) > 0) {
          return CALL_NEXT_OP; // rewind
        }
        return c.compare(buffer, stop) > 0 ? RELEASE : TERMINATE;
      case BACKWARD_GREATER_THAN:
        return c.compare(buffer, start) >= 0 ? CALL_NEXT_OP : RELEASE;
      case BACKWARD_LESS_THAN:
        return c.compare(buffer, stop) > 0 ? RELEASE : TERMINATE;
      case BACKWARD_OPEN:
        if (c.compare(buffer, start) >= 0) {
          return CALL_NEXT_OP; // rewind
        }
        return c.compare(buffer, stop) > 0 ? RELEASE : TERMINATE;
      case BACKWARD_OPEN_CLOSED:
        if (c.compare(buffer, start) >= 0) {
          return CALL_NEXT_OP; // rewind
        }
        return c.compare(buffer, stop) >= 0 ? RELEASE : TERMINATE;
      default:
        throw new IllegalStateException("Invalid type");
    }
  }
```
[ ] logfellow--logstash-logback-encoder--appendRootCauseLast
https://github.com/logfellow/logstash-logback-encoder/blob/c2a913a5220b0b8c3623bdc357d312c3e6681894/./src/main/java/net/logstash/logback/stacktrace/ShortenedThrowableConverter.java#L412-L439
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
[ ] logfellow--logstash-logback-encoder--getMaskedValueForCurrentPath
https://github.com/logfellow/logstash-logback-encoder/blob/c2a913a5220b0b8c3623bdc357d312c3e6681894/./src/main/java/net/logstash/logback/mask/MaskingJsonGenerator.java#L513-L526
```
    /**
     * @return the masked value for the current path if the current path should be masked.
     *         otherwise returns null.
     */
    private Object getMaskedValueForCurrentPath() {
        JsonStreamContext context = getOutputContext();
        for (FieldMasker fieldMasker : fieldMaskers) {
            Object maskedValue = fieldMasker.mask(context);
            if (maskedValue != null) {
                return maskedValue;
            }
        }
        return null;
    }
```
[ ] logfellow--logstash-logback-encoder--isBlank
https://github.com/logfellow/logstash-logback-encoder/blob/c2a913a5220b0b8c3623bdc357d312c3e6681894/./src/main/java/net/logstash/logback/util/StringUtils.java#L131-L158
```
    /**
     * <p>Checks if a CharSequence is empty (""), null or whitespace only.</p>
     *
     * <p>Whitespace is defined by {@link Character#isWhitespace(char)}.</p>
     *
     * <pre>
     * StringUtils.isBlank(null)      = true
     * StringUtils.isBlank("")        = true
     * StringUtils.isBlank(" ")       = true
     * StringUtils.isBlank("bob")     = false
     * StringUtils.isBlank("  bob  ") = false
     * </pre>
     *
     * @param cs the CharSequence to check, may be null
     * @return {@code true} if the CharSequence is null, empty or whitespace only
     */
    public static boolean isBlank(final CharSequence cs) {
        final int strLen = length(cs);
        if (strLen == 0) {
            return true;
        }
        for (int i = 0; i < strLen; i++) {
            if (!Character.isWhitespace(cs.charAt(i))) {
                return false;
            }
        }
        return true;
    }
```
[ ] logfellow--logstash-logback-encoder--shouldAppendPackagingData
https://github.com/logfellow/logstash-logback-encoder/blob/c2a913a5220b0b8c3623bdc357d312c3e6681894/./src/main/java/net/logstash/logback/stacktrace/ShortenedThrowableConverter.java#L652-L666
```
    /**
     * Return true if packaging data should be appended for the current step.
     *
     * Packaging data for the current step is only appended if it differs
     * from the packaging data from the previous step.
     */
    private boolean shouldAppendPackagingData(StackTraceElementProxy step, StackTraceElementProxy previousStep) {
        if (step.getClassPackagingData() == null) {
            return false;
        }
        if (previousStep == null || previousStep.getClassPackagingData() == null) {
            return true;
        }
        return !step.getClassPackagingData().equals(previousStep.getClassPackagingData());
    }
```
[ ] making--yavi--bestEffortCount
https://github.com/making/yavi/blob/d8a15ed764980eeb3ecd8d01fec42f6ecaf01899/./src/main/java/am/ik/yavi/constraint/charsequence/Emoji.java#L58-L81
```
	/**
	 * Try to return the length of the given string.<br>
	 * This method does not grantee the exact length.
	 * @see <a href="https://unicode.org/Public/emoji/12.0/emoji-test.txt">Emoji 12.0</a>
	 * @param str
	 * @return the length of the given string which may be true
	 */
	public static int bestEffortCount(@Nullable String str) {
		if (str == null || str.isEmpty()) {
			return 0;
		}
		String s = str.replaceAll("[" + StandardizedVariationSequence.RANGE + COMBINING_ENCLOSING_KEYCAP + "]", "") //
			.replaceAll("([" + WHITE_UP_POINTING_INDEX + "-" + ELF + E140_SKIN_RANGE + "][" + SKIN_TONE_SELECTOR_RANGE
					+ "])", DUMMY_REPLACEMENT)
			.replaceAll("([" + ZERO_WIDTH_JOINER + "][" + SKUL_AND_CROSSBONES + "-" + PERSON + ADHESIVE_BANDAGE + "])",
					"") //
			.replaceAll("([" + REGIONAL_INDICATOR_SYMBOL_LETTER_RANGE + "]{2})", DUMMY_REPLACEMENT) //
			.replace(ENGLAND, DUMMY_REPLACEMENT) //
			.replace(SCOTLAND, DUMMY_REPLACEMENT) //
			.replace(WALES, DUMMY_REPLACEMENT) //
			// Support emojis that contains two skin tone selectors introduced in 12
			.replaceAll("(" + DUMMY_REPLACEMENT + ZERO_WIDTH_JOINER + DUMMY_REPLACEMENT + ")", DUMMY_REPLACEMENT);
		return s.codePointCount(0, s.length());
	}
```
[x] mangiucugna--json_repair--parse_comment
https://github.com/mangiucugna/json_repair/blob/7ca4d6de56ab3824f617e913ee5003171a044578/./src/json_repair/parse_comment.py#L10-L71
```
def parse_comment(self: "JSONParser") -> JSONReturnType:
    """
    Parse code-like comments:

    - "# comment": A line comment that continues until a newline.
    - "// comment": A line comment that continues until a newline.
    - "/* comment */": A block comment that continues until the closing delimiter "*/".

    The comment is skipped over and an empty string is returned so that comments do not interfere
    with the actual JSON elements.
    """
    char = self.get_char_at()
    termination_characters = ["\n", "\r"]
    if ContextValues.ARRAY in self.context.context:
        termination_characters.append("]")
    if ContextValues.OBJECT_VALUE in self.context.context:
        termination_characters.append("}")
    if ContextValues.OBJECT_KEY in self.context.context:
        termination_characters.append(":")
    # Line comment starting with #
    if char == "#":
        comment = ""
        while char and char not in termination_characters:
            comment += char
            self.index += 1
            char = self.get_char_at()
        self.log(f"Found line comment: {comment}, ignoring")
    # Comments starting with '/'
    elif char == "/":
        next_char = self.get_char_at(1)
        # Handle line comment starting with //
        if next_char == "/":
            comment = "//"
            self.index += 2  # Skip both slashes.
            char = self.get_char_at()
            while char and char not in termination_characters:
                comment += char
                self.index += 1
                char = self.get_char_at()
            self.log(f"Found line comment: {comment}, ignoring")
        # Handle block comment starting with /*
        elif next_char == "*":
            comment = "/*"
            self.index += 2  # Skip '/*'
            while True:
                char = self.get_char_at()
                if not char:
                    self.log("Reached end-of-string while parsing block comment; unclosed block comment.")
                    break
                comment += char
                self.index += 1
                if comment.endswith("*/"):
                    break
            self.log(f"Found block comment: {comment}, ignoring")
        else:
            # Skip standalone '/' characters that are not part of a comment
            # to avoid getting stuck in an infinite loop
            self.index += 1
    if self.context.empty:
        return self.parse_json()
    else:
        return ""
```
[ ] mangiucugna--json_repair--repair_json
https://github.com/mangiucugna/json_repair/blob/7ca4d6de56ab3824f617e913ee5003171a044578/./src/json_repair/json_repair.py#L60-L104
```
def repair_json(
    json_str: str = "",
    return_objects: bool = False,
    skip_json_loads: bool = False,
    logging: bool = False,
    json_fd: TextIO | None = None,
    chunk_length: int = 0,
    stream_stable: bool = False,
    **json_dumps_args,
) -> JSONReturnType | tuple[JSONReturnType, list[dict[str, str]]] | tuple[JSONReturnType, list]:
    """
    Given a json formatted string, it will try to decode it and, if it fails, it will try to fix it.

    Args:
        json_str (str, optional): The JSON string to repair. Defaults to an empty string.
        return_objects (bool, optional): If True, return the decoded data structure. Defaults to False.
        skip_json_loads (bool, optional): If True, skip calling the built-in json.loads() function to verify that the json is valid before attempting to repair. Defaults to False.
        logging (bool, optional): If True, return a tuple with the repaired json and a log of all repair actions. Defaults to False. When no repairs were required, the repair log will be an empty list.
        json_fd (Optional[TextIO], optional): File descriptor for JSON input. Do not use! Use `from_file` or `load` instead. Defaults to None.
        ensure_ascii (bool, optional): Set to False to avoid converting non-latin characters to ascii (for example when using chinese characters). Defaults to True. Ignored if `skip_json_loads` is True.
        chunk_length (int, optional): Size in bytes of the file chunks to read at once. Ignored if `json_fd` is None. Do not use! Use `from_file` or `load` instead. Defaults to 1MB.
        stream_stable (bool, optional): When the json to be repaired is the accumulation of streaming json at a certain moment.If this parameter to True will keep the repair results stable.
    Returns:
        Union[JSONReturnType, Tuple[JSONReturnType, List[Dict[str, str]]]]: The repaired JSON or a tuple with the repaired JSON and repair log when logging is True.
    """
    parser = JSONParser(json_str, json_fd, logging, chunk_length, stream_stable)
    if skip_json_loads:
        parsed_json = parser.parse()
    else:
        try:
            parsed_json = json.load(json_fd) if json_fd else json.loads(json_str)
        except json.JSONDecodeError:
            parsed_json = parser.parse()
    # It's useful to return the actual object instead of the json string,
    # it allows this lib to be a replacement of the json library
    if return_objects or logging:
        # If logging is True, the user should expect a tuple.
        # If json.load(s) worked, the repair log list is empty
        if logging and not isinstance(parsed_json, tuple):
            return parsed_json, []
        return parsed_json
    # Avoid returning only a pair of quotes if it's an empty string
    elif parsed_json == "":
        return ""
    return json.dumps(parsed_json, **json_dumps_args)
```
[ ] mangiucugna--json_repair--skip_to_character
https://github.com/mangiucugna/json_repair/blob/7ca4d6de56ab3824f617e913ee5003171a044578/./src/json_repair/json_parser.py#L158-L176
```
    def skip_to_character(self, character: str | list, idx: int = 0) -> int:
        """
        This function quickly iterates to find a character, syntactic sugar to make the code more concise
        """
        try:
            char = self.json_str[self.index + idx]
        except IndexError:
            return idx
        character_list = character if isinstance(character, list) else [character]
        while char not in character_list:
            idx += 1
            try:
                char = self.json_str[self.index + idx]
            except IndexError:
                return idx
        if self.json_str[self.index + idx - 1] == "\\":
            # Ah shoot this was actually escaped, continue
            return self.skip_to_character(character, idx + 1)
        return idx
```
[ ] marshmallow-code--webargs--is_json
https://github.com/marshmallow-code/webargs/blob/8838ea17702ac4a23721f8a0002ef77e87336cf0/./src/webargs/core.py#L88-L101
```
def is_json(mimetype: str | None) -> bool:
    """Indicates if this mimetype is JSON or not.  By default a request
    is considered to include JSON data if the mimetype is
    ``application/json`` or ``application/*+json``.
    """
    if not mimetype:
        return False
    if ";" in mimetype:  # Allow Content-Type header to be passed
        mimetype = get_mimetype(mimetype)
    if mimetype == "application/json":
        return True
    if mimetype.startswith("application/") and mimetype.endswith("+json"):
        return True
    return False
```
[ ] meta-llama--synthetic-data-kit--chat_completion
https://github.com/meta-llama/synthetic-data-kit/blob/27a5541b2cc3537954c381eafc5398ab0838a397/./synthetic_data_kit/models/llm_client.py#L131-L158
```
    def chat_completion(self, 
                      messages: List[Dict[str, str]], 
                      temperature: float = None, 
                      max_tokens: int = None,
                      top_p: float = None) -> str:
        """Generate a chat completion using the selected provider
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (higher = more random)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            
        Returns:
            String containing the generated text
        """
        # Get defaults from config if not provided
        generation_config = self.config.get('generation', {})
        temperature = temperature if temperature is not None else generation_config.get('temperature', 0.1)
        max_tokens = max_tokens if max_tokens is not None else generation_config.get('max_tokens', 4096)
        top_p = top_p if top_p is not None else generation_config.get('top_p', 0.95)
        
        verbose = os.environ.get('SDK_VERBOSE', 'false').lower() == 'true'
        
        if self.provider == 'api-endpoint':
            return self._openai_chat_completion(messages, temperature, max_tokens, top_p, verbose)
        else:  # Default to vLLM
            return self._vllm_chat_completion(messages, temperature, max_tokens, top_p, verbose)
```
[x] mhewedy--spring-data-jpa-mongodb-expressions--getExpressions
https://github.com/mhewedy/spring-data-jpa-mongodb-expressions/blob/c1351727560a1acb1dbc0e1c0b902a77d5bae904/./src/main/java/com/github/mhewedy/expressions/Expressions.java#L180-L231
```
    /**
     * Returns this object as list of {@link Expression} to be passed to
     * Spring Data Specification builder {@link ExpressionsPredicateBuilder}
     */
    @SuppressWarnings({"unchecked"})
    private static List<Expression> getExpressions(Map<String, Object> map) {

        List<Expression> expressions = new ArrayList<>();

        for (Entry<String, Object> entry : map.entrySet()) {

            String key = entry.getKey();
            Object value = entry.getValue();

            if ($or.name().equalsIgnoreCase(key)) {
                List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;

                OrExpression orExpression = new OrExpression();
                expressions.add(orExpression);

                for (Map<String, Object> valueMap : valueList) {
                    orExpression.expressions.add(getExpressions(valueMap).get(0));
                }
            } else if ($and.name().equalsIgnoreCase(key)) {
                List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;

                AndExpression andExpression = new AndExpression();
                expressions.add(andExpression);

                for (Map<String, Object> valueMap : valueList) {
                    andExpression.expressions.add(getExpressions(valueMap).get(0));
                }
            } else {
                if (value instanceof Map) { // value in the form of {"$operator": "value"}
                    Map<String, Object> valueMap = ((Map<String, Object>) value);
                    Entry<String, Object> first = valueMap.entrySet().iterator().next();

                    Operator operator = Operator.valueOf(first.getKey());

                    if (operator.isList) {
                        expressions.add(new ListExpression(key, operator, first.getValue()));
                    } else {
                        expressions.add(new SingularExpression(key, operator, first.getValue()));
                    }
                } else { // operator is "$eq"
                    expressions.add(new SingularExpression(key, Operator.$eq, value));
                }
            }
        }

        return expressions;
    }
```
[ ] mirromutth--r2dbc-mysql--findParamMark
https://github.com/mirromutth/r2dbc-mysql/blob/ba5401f05740752290979aa76b23caea6a3afdde/./src/main/java/dev/miku/r2dbc/mysql/Query.java#L225-L314
```
    /**
     * Locates the first occurrence of {@literal ?} return true in {@code sql} starting at {@code offset}.
     * <p>
     * The SQL string may contain:
     *
     * <ul>
     * <li>Literals, enclosed in single quotes ({@literal '}) </li>
     * <li>Literals, enclosed in double quotes ({@literal "}) </li>
     * <li>Literals, enclosed in backtick quotes ({@literal `}) </li>
     * <li>Escaped escapes or literal delimiters (i.e. {@literal ''}, {@literal ""} or {@literal ``})</li>
     * <li>Single-line comments beginning with {@literal --}</li>
     * <li>Multi-line comments beginning enclosed</li>
     * </ul>
     *
     * @param sql   the SQL string to search in.
     * @param start the offset to start searching.
     * @return the offset or a negative integer if not found.
     */
    private static int findParamMark(CharSequence sql, int start) {
        int offset = start;
        int length = sql.length();
        char ch;

        while (offset < length && offset >= 0) {
            ch = sql.charAt(offset++);
            switch (ch) {
                case '/':
                    if (offset == length) {
                        break;
                    }

                    if (sql.charAt(offset) == '*') {
                        // Consume if '/* ... */' comment.
                        while (++offset < length) {
                            if (sql.charAt(offset) == '*' && offset + 1 < length &&
                                sql.charAt(offset + 1) == '/') {
                                // If end of comment.
                                offset += 2;
                                break;
                            }
                        }
                        break;
                    }

                    break;
                case '-':
                    if (offset == length) {
                        break;
                    }

                    if (sql.charAt(offset) == '-') {
                        // Consume if '-- ... \n' comment.
                        while (++offset < length) {
                            char now = sql.charAt(offset);
                            if (now == '\n' || now == '\r') {
                                // If end of comment
                                offset++;
                                break;
                            }
                        }
                        break;
                    }

                    break;
                case '`':
                case '\'':
                case '"':
                    // Quote cases, should find same quote
                    while (offset < length) {
                        if (sql.charAt(offset++) == ch) {
                            if (length == offset || sql.charAt(offset) != ch) {
                                break;
                            }

                            ++offset;
                        }
                    }

                    break;
                default:
                    if (ch == '?') {
                        return offset - 1;
                    }

                    break;
            }
        }

        return -1;
    }
```
[ ] miyuchina--mistletoe--children
https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/token.py#L88-L98
```
    @children.setter
    def children(self, value: Iterable['Token']):
        """"
        Sets new child (nested) tokens.
        Passed tokens are iterated and their ``parent`` property is set to
        this token.
        """
        self._children = value
        if value:
            for child in value:
                child._parent = self
```
[ ] miyuchina--mistletoe--get_ast
https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/ast_renderer.py#L22-L47
```
def get_ast(token):
    """
    Recursively unrolls token attributes into dictionaries (token.children
    into lists).

    Returns:
        a dictionary of token's attributes.
    """
    node = {}
    # Python 3.6 uses [ordered dicts] [1].
    # Put in 'type' entry first to make the final tree format somewhat
    # similar to [MDAST] [2].
    #
    #   [1]: https://docs.python.org/3/whatsnew/3.6.html
    #   [2]: https://github.com/syntax-tree/mdast
    node['type'] = token.__class__.__name__
    for attrname in ['content', 'footnotes']:
        if attrname in vars(token):
            node[attrname] = getattr(token, attrname)
    for attrname in token.repr_attributes:
        node[attrname] = getattr(token, attrname)
    if 'header' in vars(token):
        node['header'] = get_ast(getattr(token, 'header'))
    if token.children is not None:
        node['children'] = [get_ast(child) for child in token.children]
    return node
```
[ ] miyuchina--mistletoe--parse_align
https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/block_token.py#L737-L747
```
    @staticmethod
    def parse_align(column):
        """
        Helper function; returns align option from cell content.

        Returns:
            None if align = left;
            0    if align = center;
            1    if align = right.
        """
        return (0 if column[0] == ':' else 1) if column[-1] == ':' else None
```
[ ] miyuchina--mistletoe--parse_marker
https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/block_token.py#L590-L618
```
    @classmethod
    def parse_marker(cls, line):
        """
        Returns a tuple (prepend, leader, content) iff the line has a valid leader and at
        least one space separating leader and content, or if the content is empty, in which
        case there need not be any spaces.
        The return value is None if the line doesn't have a valid marker.

        The leader is a bullet list marker, or an ordered list marker.

        The indentation is spaces before the leader.

        The prepend is the start position of the content, i.e., the indentation required
        for continuation lines.
        """
        match_obj = cls.pattern.match(line)
        if match_obj is None:
            return None
        indentation = len(match_obj.group(1))
        prepend = len(match_obj.group(0).expandtabs(4))
        leader = match_obj.group(2)
        content = line[match_obj.end(0):]
        n_spaces = prepend - match_obj.end(2)
        if n_spaces > 4:
            # if there are more than 4 spaces after the leader, we treat them as part of the content
            # with the exception of the first (marker separator) space.
            prepend -= n_spaces - 1
            content = ' ' * (n_spaces - 1) + content
        return indentation, prepend, leader, content
```
[ ] mojohaus--jaxb2-maven-plugin--onCandidate
https://github.com/mojohaus/jaxb2-maven-plugin/blob/3703a9e9a174aae4aa4ce682487c6e1c3f056786/./src/main/java/org/codehaus/mojo/jaxb2/shared/filters/pattern/AbstractPatternFilter.java#L175-L232
```
    /**
     * <p>Each nonNullCandidate is matched against all Patterns supplied to this AbstractPatternFilter.
     * The match table of this AbstractPatternFilter on each candidate is as follows:</p>
     * <table>
     * <caption>Truth table for the onCandidate method</caption>
     * <tr>
     * <th style="background: #eeeeee">at least 1 filter matches</th>
     * <th style="background: #eeeeee">acceptCandidateOnPatternMatch</th>
     * <th style="background: #eeeeee">result</th>
     * </tr>
     * <tr>
     * <td style="border: 1px solid #dddddd">true</td>
     * <td style="border: 1px solid #dddddd">true</td>
     * <td style="border: 1px solid #dddddd">true</td>
     * </tr>
     * <tr>
     * <td style="border: 1px solid #dddddd">false</td>
     * <td style="border: 1px solid #dddddd">true</td>
     * <td style="border: 1px solid #dddddd">false</td>
     * </tr>
     * <tr>
     * <td style="border: 1px solid #dddddd">true</td>
     * <td style="border: 1px solid #dddddd">false</td>
     * <td style="border: 1px solid #dddddd">false</td>
     * </tr>
     * <tr>
     * <td style="border: 1px solid #dddddd">false</td>
     * <td style="border: 1px solid #dddddd">false</td>
     * <td style="border: 1px solid #dddddd">true</td>
     * </tr>
     * </table>
     * {@inheritDoc}
     */
    @Override
    protected boolean onCandidate(final T nonNullCandidate) {

        final String candidateString = convert(nonNullCandidate);
        boolean atLeastOnePatternMatched = false;

        if (regularExpressions != null) {
            for (Pattern current : regularExpressions) {
                if (current.matcher(candidateString).matches()) {

                    if (log.isDebugEnabled()) {
                        log.debug("CandidateString [" + candidateString + "] matched pattern [" + current.pattern()
                                + "]");
                    }

                    // Adjust and return
                    atLeastOnePatternMatched = true;
                    break;
                }
            }
        }

        // Apply the reverse match logic if applicable
        return acceptCandidateOnPatternMatch ? atLeastOnePatternMatched : !atLeastOnePatternMatched;
    }
```
[ ] mongomock--mongomock--_get_subdocument
https://github.com/mongomock/mongomock/blob/edd20d32254179c5373b81143a0bc2e7e7fe24a6/./mongomock/collection.py#L1168-L1221
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) - 1:
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
[x] mongomock--mongomock--_iter_key_candidates_sublist
https://github.com/mongomock/mongomock/blob/edd20d32254179c5373b81143a0bc2e7e7fe24a6/./mongomock/filtering.py#L252-L283
```
def _iter_key_candidates_sublist(key, doc):
    """Iterates of candidates

    :param doc: a list to be searched for candidates for our key
    :param key: the string key to be matched
    """
    key_parts = key.split('.')
    sub_key = key_parts.pop(0)
    key_remainder = '.'.join(key_parts)
    try:
        sub_key_int = int(sub_key)
    except ValueError:
        sub_key_int = None

    if sub_key_int is None:
        # subkey is not an integer...
        ret = []
        for sub_doc in doc:
            if isinstance(sub_doc, dict):
                if sub_key in sub_doc:
                    ret.extend(iter_key_candidates(key_remainder, sub_doc[sub_key]))
                else:
                    ret.append(NOTHING)
        return ret

    # subkey is an index
    if sub_key_int >= len(doc):
        return ()  # dead end
    sub_doc = doc[sub_key_int]
    if key_parts:
        return iter_key_candidates('.'.join(key_parts), sub_doc)
    return [sub_doc]
```
[ ] mvallim--emv-qrcode--crc16
https://github.com/mvallim/emv-qrcode/blob/328ae292cce8d0f40b071b4b8ccab64a63e2c3b2/./src/main/java/com/emv/qrcode/core/CRC.java#L25-L60
```
  /**
   * Information technology—Telecommunications and information exchange between
   * systems—High-level data link control (HDLC) procedures.
   *
   * The checksum shall be calculated according to [ISO/IEC 13239] using the
   * polynomial '1021' (hex) and initial value 'FFFF' (hex).
   *
   * Implements CRC-16/CCITT-FALSE
   *
   * @see https://en.wikipedia.org/wiki/Cyclic_redundancy_check
   *
   * @param value
   * @return CRC16 integer
   */
  public static int crc16(final byte[] value) {
    final int polynomial = 0x1021; // 0001 0000 0010 0001 (0, 5, 12)

    int result = 0xFFFF; // initial value

    final byte[] bytes = value;

    for (final byte b : bytes) {
      for (int i = 0; i < 8; i++) {
        final boolean bit = (b >> 7 - i & 1) == 1;
        final boolean c15 = (result >> 15 & 1) == 1;
        result <<= 1;
        if (c15 ^ bit) {
          result ^= polynomial;
        }
      }
    }

    result &= 0xffff;

    return result;
  }
```
[ ] mvallim--java-fluent-validator--init
https://github.com/mvallim/java-fluent-validator/blob/37ddfa4bde71e8cc8552ed085e86c6d32e7ea297/./src/main/java/br/com/fluentvalidator/AbstractValidator.java#L58-L75
```
    /**
     * This method cause Race Condition. We are using Compare And Swap (CAS)
     * <p>
     * {@link https://en.wikipedia.org/wiki/Race_condition}
     * {@link https://en.wikipedia.org/wiki/Compare-and-swap}
     */
    public void init() {
      if (isNotInitialized()) {
        synchronized (atomicReference) {
          if (isNotInitialized()) { // double check if was initialized
            validator.rules();
            final Boolean oldValue = atomicReference.get();
            final Boolean newValue = Boolean.TRUE;
            atomicReference.compareAndSet(oldValue, newValue);
          }
        }
      }
    }
```
[ ] nRo--DataFrame--addColumn
https://github.com/nRo/DataFrame/blob/a84dc2272c18a19963e742dfc2e68910442a292d/./src/main/java/de/unknownreality/dataframe/DefaultDataFrame.java#L282-L308
```
    /**
     * {@inheritDoc}
     * If no column appender is specified, the column is filled with {@link Values#NA NA} values.
     * If the column can not be created or added a {@link DataFrameRuntimeException} is thrown.
     */
    @Override
    public <T, C extends DataFrameColumn<T, C>> DataFrame addColumn(Class<C> type, String name,
                                                                    ColumnAppender<T> appender) {
        C col = type.cast(DataFrameTypeManager.get().createColumn(type));
        col.setName(name);
        if (appender != null) {
            for (DataRow row : this) {
                T val = appender.createRowValue(row);
                if (val == null || val == Values.NA) {
                    col.doAppendNA();
                } else {
                    col.doAppend(val);
                }
            }
        } else {
            for (int i = 0; i < size(); i++) {
                col.doAppendNA();
            }
        }
        addColumn(col);
        return this;
    }
```
[ ] nRo--DataFrame--isNA
https://github.com/nRo/DataFrame/blob/a84dc2272c18a19963e742dfc2e68910442a292d/./src/main/java/de/unknownreality/dataframe/Values.java#L49-L66
```
        /**
         * checks whether the input object is of type NA or null.
         *
         * @param o input object
         * @return true if the object is of type NA or null
         */
        public boolean isNA(Object o) {
            if (o == null) {
                return true;
            }
            if (o == this) {
                return true;
            }
            if (o instanceof String) {
                return "NA".equals(o.toString());
            }
            return false;
        }
```
[ ] narwhals-dev--narwhals--__eq__-2
https://github.com/narwhals-dev/narwhals/blob/bc6a77fd0c7ad7b89a0124f4aec3fe0f13e80e90/./narwhals/dtypes.py#L589-L609
```
    def __eq__(self, other: DType | type[DType]) -> bool:  # type: ignore[override]
        """Check if this Duration is equivalent to another DType.

        Examples:
            >>> import narwhals as nw
            >>> nw.Duration("us") == nw.Duration("us")
            True
            >>> nw.Duration() == nw.Duration("us")
            True
            >>> nw.Duration("us") == nw.Duration("ns")
            False
            >>> nw.Duration() == nw.Datetime()
            False
            >>> nw.Duration("ms") == nw.Duration
            True
        """
        if type(other) is _DurationMeta:
            return True
        if isinstance(other, self.__class__):
            return self.time_unit == other.time_unit
        return False  # pragma: no cover
```
[ ] narwhals-dev--narwhals--__eq__-3
https://github.com/narwhals-dev/narwhals/blob/bc6a77fd0c7ad7b89a0124f4aec3fe0f13e80e90/./narwhals/dtypes.py#L785-L808
```
    def __eq__(self, other: DType | type[DType]) -> bool:  # type: ignore[override]
        """Check if this Struct is equivalent to another DType.

        Examples:
            >>> import narwhals as nw
            >>> nw.Struct({"a": nw.Int64}) == nw.Struct({"a": nw.Int64})
            True
            >>> nw.Struct({"a": nw.Int64}) == nw.Struct({"a": nw.Boolean})
            False
            >>> nw.Struct({"a": nw.Int64}) == nw.Struct({"b": nw.Int64})
            False
            >>> nw.Struct({"a": nw.Int64}) == nw.Struct([nw.Field("a", nw.Int64)])
            True

            If a parent type is not specific about its inner type, we infer it as equal

            >>> nw.Struct({"a": nw.Int64}) == nw.Struct
            True
        """
        if type(other) is type and issubclass(other, self.__class__):
            return True
        if isinstance(other, self.__class__):
            return self.fields == other.fields
        return False
```
[ ] narwhals-dev--narwhals--clip
https://github.com/narwhals-dev/narwhals/blob/bc6a77fd0c7ad7b89a0124f4aec3fe0f13e80e90/./narwhals/expr.py#L1546-L1582
```
    def clip(
        self,
        lower_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
        upper_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
    ) -> Self:
        r"""Clip values in the Series.

        Arguments:
            lower_bound: Lower bound value. String literals are treated as column names.
            upper_bound: Upper bound value. String literals are treated as column names.

        Examples:
            >>> import pandas as pd
            >>> import narwhals as nw
            >>> df_native = pd.DataFrame({"a": [1, 2, 3]})
            >>> df = nw.from_native(df_native)
            >>> df.with_columns(a_clipped=nw.col("a").clip(-1, 3))
            ┌──────────────────┐
            |Narwhals DataFrame|
            |------------------|
            |    a  a_clipped  |
            | 0  1          1  |
            | 1  2          2  |
            | 2  3          3  |
            └──────────────────┘
        """
        if upper_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_lower", lower_bound)
            )
        if lower_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound)
            )
        return self._append_node(
            ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
        )
```
[ ] networknt--json-schema-validator--buildIndex
https://github.com/networknt/json-schema-validator/blob/a8bda4c9f43f17f657513083c0ae6f9690e51b9b/./src/main/java/com/networknt/schema/output/HierarchicalOutputUnitFormatter.java#L125-L178
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
[ ] networknt--json-schema-validator--get
https://github.com/networknt/json-schema-validator/blob/a8bda4c9f43f17f657513083c0ae6f9690e51b9b/./src/main/java/com/networknt/schema/CollectorContext.java#L84-L104
```
    /**
     * Gets the data associated with a given name. Please note if you are collecting
     * {@link Collector} instances you should wait till the validation is complete
     * to gather all data.
     * <p>
     * When {@link CollectorContext} is used to collect {@link Collector} instances
     * for a particular key, this method will return the {@link Collector} instance
     * as long as {@link #loadCollectors} method is not called. Once
     * the {@link #loadCollectors} method is called this method will
     * return the actual data collected by collector.
     *
     * @param name String
     * @return Object
     */
    public Object get(String name) {
        Object object = this.collectorMap.get(name);
        if (object instanceof Collector<?> && (this.collectorLoadMap.get(name) != null)) {
            return this.collectorLoadMap.get(name);
        }
        return this.collectorMap.get(name);
    }
```
[ ] nikoo28--java-solutions--move
https://github.com/nikoo28/java-solutions/blob/a7f282d36a96a486af2259f5fd15deb96b00667a/./src/main/java/leetcode/medium/TicTacToe.java#L50-L78
```
  /**
   * Player {player} makes a move at ({row}, {col}).
   *
   * @param row    The row of the board.
   * @param col    The column of the board.
   * @param player The player, can be either 1 or 2.
   * @return The current winning condition, can be either:
   * 0: No one wins.
   * 1: Player 1 wins.
   * 2: Player 2 wins.
   */
  int move(int row, int col, int player) {

    char c = player == 1 ? 'X' : 'O';

    Tuple rowNumber = rows.get(row);
    Tuple colNumber = cols.get(col);

    processTuple(rowNumber, c);
    processTuple(colNumber, c);

    // Handle left diagonal
    if (row == col) processTuple(leftDiagonal, c);

    // Handle right diagonal
    if (row + col == gridSize - 1) processTuple(rightDiagonal, c);

    return checkResult(player, gridSize);
  }
```
[ ] nikoo28--java-solutions--search
https://github.com/nikoo28/java-solutions/blob/a7f282d36a96a486af2259f5fd15deb96b00667a/./src/main/java/leetcode/medium/SearchInRotatedSortedArray.java#L78-L93
```
  /**
   * Search by first finding the rotation index. The index about which the array has been rotated.
   * Then compare the target value to do a simple binary search in the left sub-array or right sub-array.
   */
  public int search(int[] nums, int target) {

    int rotationIndex = findRotationIndex(nums);

    if (rotationIndex == -1 || rotationIndex == nums.length - 1)
      return binarySearch(nums, 0, nums.length - 1, target);

    if (nums[0] <= target) {
      return binarySearch(nums, 0, rotationIndex, target);
    } else
      return binarySearch(nums, rotationIndex + 1, nums.length - 1, target);
  }
```
[ ] nikoo28--java-solutions--sherlockAndCostProblem
https://github.com/nikoo28/java-solutions/blob/a7f282d36a96a486af2259f5fd15deb96b00667a/./src/main/java/hackerrank/algorithms/dynamicprogramming/SherLockAndCost.java#L7-L31
```
  /**
   * Approach:
   * I can use dynamic programming to solve this problem efficiently. Let’s break down the approach:
   * <p>
   * 1.) Initialize two arrays: dp[i][0] and dp[i][1]. These arrays will store the maximum sum of absolute differences for the first i elements of the input array.
   * 2.) Iterate through the input array from left to right:
   * Update dp[i][0] and dp[i][1] based on the previous values and the current element.
   * 3.) The final answer is the maximum value between dp[N-1][0] and dp[N-1][1].
   */
  int sherlockAndCostProblem(List<Integer> list) {
    int N = list.size();
    int[][] dp = new int[N][2];
    dp[0][0] = 0;
    dp[0][1] = 0;

    for (int i = 1; i < N; i++) {
      int curr = list.get(i);
      int prev = list.get(i - 1);

      dp[i][0] = Math.max(dp[i - 1][0], dp[i - 1][1] + prev - 1);
      dp[i][1] = Math.max(dp[i - 1][1], dp[i - 1][0] + curr - 1);
    }

    return Math.max(dp[N - 1][0], dp[N - 1][1]);
  }
```
[ ] nschloe--matplotx--_move_min_distance
https://github.com/nschloe/matplotx/blob/4e536bcd05b39a320a5f04e67e5c99a4e4e49f67/./src/matplotx/_labels.py#L13-L37
```
def _move_min_distance(targets: ArrayLike, min_distance: float) -> np.ndarray:
    """Move the targets such that they are close to their original positions, but keep
    min_distance apart.

    https://math.stackexchange.com/a/3705240/36678
    """
    # sort targets
    idx = np.argsort(targets)
    targets = np.sort(targets)

    n = len(targets)
    x0_min = targets[0] - n * min_distance
    A = np.tril(np.ones([n, n]))
    b = targets - (x0_min + np.arange(n) * min_distance)

    # import scipy.optimize
    # out, _ = scipy.optimize.nnls(A, b)

    out = nnls(A, b)

    sol = np.cumsum(out) + x0_min + np.arange(n) * min_distance

    # reorder
    idx2 = np.argsort(idx)
    return sol[idx2]
```
[ ] opentracing-contrib--java-jdbc--parseEasyConnect
https://github.com/opentracing-contrib/java-jdbc/blob/6722745cbbd61fce8550dd8e1e0d8a828a1e7a3c/./src/main/java/io/opentracing/contrib/jdbc/parser/OracleURLParser.java#L115-L139
```
  /**
   * Implementation according to https://www.oracle.com/technetwork/database/enterprise-edition/oraclenetservices-neteasyconnect-133058.pdf
   *
   * @param url the url without the oracle jdbc prefix
   * @return the oracle connection info if the url could be parsed, or null otherwise.
   */
  public static OracleConnectionInfo parseEasyConnect(final String url) {
    final Matcher matcher = EASY_CONNECT_PATTERN.matcher(url);
    if (matcher.matches()) {
      final OracleConnectionInfo result = new OracleConnectionInfo();
      final String host = matcher.group("host");
      final String portGroup = matcher.group("port");
      final int dbPort =
          portGroup != null ? Integer.parseInt(portGroup.substring(1)) : DEFAULT_PORT;
      result.setDbPeer(host + ":" + dbPort);
      final String service = matcher.group("service");
      if (service != null) {
        result.setDbInstance(service.substring(1));
      } else {
        result.setDbInstance(host);
      }
      return result;
    }
    return null;
  }
```
[ ] pallets--flask--_called_with_wrong_args
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/cli.py#L94-L117
```
def _called_with_wrong_args(f: t.Callable[..., Flask]) -> bool:
    """Check whether calling a function raised a ``TypeError`` because
    the call failed or because something in the factory raised the
    error.

    :param f: The function that was called.
    :return: ``True`` if the call failed.
    """
    tb = sys.exc_info()[2]

    try:
        while tb is not None:
            if tb.tb_frame.f_code is f.__code__:
                # In the function, it was called successfully.
                return False

            tb = tb.tb_next

        # Didn't reach the function.
        return True
    finally:
        # Delete tb to break a circular reference.
        # https://docs.python.org/2/library/sys.html#sys.exc_info
        del tb
```
[ ] pallets--flask--_find_error_handler
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/sansio/app.py#L871-L894
```
    def _find_error_handler(
        self, e: Exception, blueprints: list[str]
    ) -> ft.ErrorHandlerCallable | None:
        """Return a registered error handler for an exception in this order:
        blueprint handler for a specific code, app handler for a specific code,
        blueprint handler for an exception class, app handler for an exception
        class, or ``None`` if a suitable handler is not found.
        """
        exc_class, code = self._get_exc_class_and_code(type(e))
        names = (*blueprints, None)

        for c in (code, None) if code is not None else (None,):
            for name in names:
                handler_map = self.error_handler_spec[name][c]

                if not handler_map:
                    continue

                for cls in exc_class.__mro__:
                    handler = handler_map.get(cls)

                    if handler is not None:
                        return handler
        return None
```
[ ] pallets--flask--create_logger
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/logging.py#L58-L79
```
def create_logger(app: App) -> logging.Logger:
    """Get the Flask app's logger and configure it if needed.

    The logger name will be the same as
    :attr:`app.import_name <flask.Flask.name>`.

    When :attr:`~flask.Flask.debug` is enabled, set the logger level to
    :data:`logging.DEBUG` if it is not set.

    If there is no handler for the logger's effective level, add a
    :class:`~logging.StreamHandler` for
    :func:`~flask.logging.wsgi_errors_stream` with a basic format.
    """
    logger = logging.getLogger(app.name)

    if app.debug and not logger.level:
        logger.setLevel(logging.DEBUG)

    if not has_level_handler(logger):
        logger.addHandler(default_handler)

    return logger
```
[ ] pallets--flask--from_mapping
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/config.py#L304-L321
```
    def from_mapping(
        self, mapping: t.Mapping[str, t.Any] | None = None, **kwargs: t.Any
    ) -> bool:
        """Updates the config like :meth:`update` ignoring items with
        non-upper keys.

        :return: Always returns ``True``.

        .. versionadded:: 0.11
        """
        mappings: dict[str, t.Any] = {}
        if mapping is not None:
            mappings.update(mapping)
        mappings.update(kwargs)
        for key, value in mappings.items():
            if key.isupper():
                self[key] = value
        return True
```
[ ] pallets--flask--from_prefixed_env
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/config.py#L126-L185
```
    def from_prefixed_env(
        self, prefix: str = "FLASK", *, loads: t.Callable[[str], t.Any] = json.loads
    ) -> bool:
        """Load any environment variables that start with ``FLASK_``,
        dropping the prefix from the env key for the config key. Values
        are passed through a loading function to attempt to convert them
        to more specific types than strings.

        Keys are loaded in :func:`sorted` order.

        The default loading function attempts to parse values as any
        valid JSON type, including dicts and lists.

        Specific items in nested dicts can be set by separating the
        keys with double underscores (``__``). If an intermediate key
        doesn't exist, it will be initialized to an empty dict.

        :param prefix: Load env vars that start with this prefix,
            separated with an underscore (``_``).
        :param loads: Pass each string value to this function and use
            the returned value as the config value. If any error is
            raised it is ignored and the value remains a string. The
            default is :func:`json.loads`.

        .. versionadded:: 2.1
        """
        prefix = f"{prefix}_"

        for key in sorted(os.environ):
            if not key.startswith(prefix):
                continue

            value = os.environ[key]
            key = key.removeprefix(prefix)

            try:
                value = loads(value)
            except Exception:
                # Keep the value as a string if loading failed.
                pass

            if "__" not in key:
                # A non-nested key, set directly.
                self[key] = value
                continue

            # Traverse nested dictionaries with keys separated by "__".
            current = self
            *parts, tail = key.split("__")

            for part in parts:
                # If an intermediate dict does not exist, create it.
                if part not in current:
                    current[part] = {}

                current = current[part]

            current[tail] = value

        return True
```
[ ] pallets--flask--get_namespace
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/config.py#L323-L364
```
    def get_namespace(
        self, namespace: str, lowercase: bool = True, trim_namespace: bool = True
    ) -> dict[str, t.Any]:
        """Returns a dictionary containing a subset of configuration options
        that match the specified namespace/prefix. Example usage::

            app.config['IMAGE_STORE_TYPE'] = 'fs'
            app.config['IMAGE_STORE_PATH'] = '/var/app/images'
            app.config['IMAGE_STORE_BASE_URL'] = 'http://img.website.com'
            image_store_config = app.config.get_namespace('IMAGE_STORE_')

        The resulting dictionary `image_store_config` would look like::

            {
                'type': 'fs',
                'path': '/var/app/images',
                'base_url': 'http://img.website.com'
            }

        This is often useful when configuration options map directly to
        keyword arguments in functions or class constructors.

        :param namespace: a configuration namespace
        :param lowercase: a flag indicating if the keys of the resulting
                          dictionary should be lowercase
        :param trim_namespace: a flag indicating if the keys of the resulting
                          dictionary should not include the namespace

        .. versionadded:: 0.11
        """
        rv = {}
        for k, v in self.items():
            if not k.startswith(namespace):
                continue
            if trim_namespace:
                key = k[len(namespace) :]
            else:
                key = k
            if lowercase:
                key = key.lower()
            rv[key] = v
        return rv
```
[ ] pallets--flask--has_level_handler
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/logging.py#L31-L47
```
def has_level_handler(logger: logging.Logger) -> bool:
    """Check if there is a handler in the logging chain that will handle the
    given logger's :meth:`effective level <~logging.Logger.getEffectiveLevel>`.
    """
    level = logger.getEffectiveLevel()
    current = logger

    while current:
        if any(handler.level <= level for handler in current.handlers):
            return True

        if not current.propagate:
            break

        current = current.parent  # type: ignore

    return False
```
[ ] pallets--flask--load_dotenv
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/cli.py#L698-L763
```
def load_dotenv(
    path: str | os.PathLike[str] | None = None, load_defaults: bool = True
) -> bool:
    """Load "dotenv" files to set environment variables. A given path takes
    precedence over ``.env``, which takes precedence over ``.flaskenv``. After
    loading and combining these files, values are only set if the key is not
    already set in ``os.environ``.

    This is a no-op if `python-dotenv`_ is not installed.

    .. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

    :param path: Load the file at this location.
    :param load_defaults: Search for and load the default ``.flaskenv`` and
        ``.env`` files.
    :return: ``True`` if at least one env var was loaded.

    .. versionchanged:: 3.1
        Added the ``load_defaults`` parameter. A given path takes precedence
        over default files.

    .. versionchanged:: 2.0
        The current directory is not changed to the location of the
        loaded file.

    .. versionchanged:: 2.0
        When loading the env files, set the default encoding to UTF-8.

    .. versionchanged:: 1.1.0
        Returns ``False`` when python-dotenv is not installed, or when
        the given path isn't a file.

    .. versionadded:: 1.0
    """
    try:
        import dotenv
    except ImportError:
        if path or os.path.isfile(".env") or os.path.isfile(".flaskenv"):
            click.secho(
                " * Tip: There are .env files present. Install python-dotenv"
                " to use them.",
                fg="yellow",
                err=True,
            )

        return False

    data: dict[str, str | None] = {}

    if load_defaults:
        for default_name in (".flaskenv", ".env"):
            if not (default_path := dotenv.find_dotenv(default_name, usecwd=True)):
                continue

            data |= dotenv.dotenv_values(default_path, encoding="utf-8")

    if path is not None and os.path.isfile(path):
        data |= dotenv.dotenv_values(path, encoding="utf-8")

    for key, value in data.items():
        if key in os.environ or value is None:
            continue

        os.environ[key] = value

    return bool(data)  # True if at least one env var was loaded.
```
[ ] pallets--flask--prepare_import
https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/cli.py#L200-L226
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "__init__.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])
```
[ ] pallets-eco--flask-pydantic--convert_query_params
https://github.com/pallets-eco/flask-pydantic/blob/7b941cc64fcf8c4a8d3214be56f91b1b6905f842/./flask_pydantic/converters.py#L40-L68
```
def convert_query_params(
    query_params: ImmutableMultiDict, model: Type[V1OrV2BaseModel]
) -> dict:
    """
    group query parameters into lists if model defines them

    :param query_params: flasks request.args
    :param model: query parameter's model
    :return: resulting parameters
    """
    if issubclass(model, BaseModel):
        return {
            **query_params.to_dict(),
            **{
                key: value
                for key, value in query_params.to_dict(flat=False).items()
                if key in model.model_fields
                and _is_sequence(model.model_fields[key].annotation)
            },
        }
    else:
        return {
            **query_params.to_dict(),
            **{
                key: value
                for key, value in query_params.to_dict(flat=False).items()
                if key in model.__fields__ and model.__fields__[key].is_complex()
            },
        }
```
[ ] pallets-eco--flask-security--default_want_json
https://github.com/pallets-eco/flask-security/blob/06f37fa06ebbb0b9e87cd6819eb44d3aea050f60/./flask_security/utils.py#L1205-L1221
```
def default_want_json(req):
    """Return True if response should be in json
    N.B. do not call this directly - use security._want_json()

    :param req: Flask/Werkzeug Request
    """
    if req.is_json:
        return True
    # TODO should this handle json sub-types?
    accept_mimetypes = req.accept_mimetypes
    if not hasattr(req.accept_mimetypes, "best"):  # pragma: no cover
        # Alright. we don't have the best property, lets add it ourselves.
        # This is for quart compatibility
        accept_mimetypes.best = best
    if accept_mimetypes.best == "application/json":
        return True
    return False
```
[ ] pallets-eco--flask-security--logout_user
https://github.com/pallets-eco/flask-security/blob/06f37fa06ebbb0b9e87cd6819eb44d3aea050f60/./flask_security/utils.py#L260-L293
```
def logout_user() -> None:
    """Logs out the current user.

    This will also clean up the remember me cookie if it exists.

    This sends an ``identity_changed`` signal to note that the current
    identity is now the `AnonymousIdentity`
    """

    for key in (
        "identity.name",
        "identity.auth_type",
        "fs_paa",
        "fs_gexp",
        "fs_oauth_next",
    ):
        session.pop(key, None)

    # Clear csrf token between sessions.
    # Ideally this would be handled by Flask-WTF but...
    # We don't clear entire session since Flask-Login seems to like having it.
    csrf_field_name = find_csrf_field_name()
    if csrf_field_name:
        session.pop(csrf_field_name, None)
        # Flask-WTF 'caches' csrf_token - and only set the session if not already
        # in 'g'. Be sure to clear both. This affects at least /confirm
        g.pop(csrf_field_name, None)
    session["fs_cc"] = "clear"
    identity_changed.send(
        current_app._get_current_object(),  # type: ignore
        _async_wrapper=current_app.ensure_sync,
        identity=AnonymousIdentity(),
    )
    _logout_user()
```
[ ] pallets-eco--flask-security--mf_delete_recovery_code
https://github.com/pallets-eco/flask-security/blob/06f37fa06ebbb0b9e87cd6819eb44d3aea050f60/./flask_security/datastore.py#L577-L592
```
    def mf_delete_recovery_code(self, user: UserMixin, idx: int) -> bool:
        """Delete a single recovery code.
        Recovery codes are single-use - so delete after using!

        Return True if code found and deleted, False otherwise.

        .. versionadded: 5.0.0
        """
        if not user.mf_recovery_codes:
            return False
        try:
            user.mf_recovery_codes.pop(idx)
            self.put(user)
            return True
        except IndexError:
            return False
```
[ ] pallets-eco--flask-sqlalchemy--__table_cls__
https://github.com/pallets-eco/flask-sqlalchemy/blob/168cb4b7b50fe5176307a10d873781bfafc6eeda/./src/flask_sqlalchemy/model.py#L152-L191
```
    def __table_cls__(cls, *args: t.Any, **kwargs: t.Any) -> sa.Table | None:
        """This is called by SQLAlchemy during mapper setup. It determines the final
        table object that the model will use.

        If no primary key is found, that indicates single-table inheritance, so no table
        will be created and ``__tablename__`` will be unset.
        """
        schema = kwargs.get("schema")

        if schema is None:
            key = args[0]
        else:
            key = f"{schema}.{args[0]}"

        # Check if a table with this name already exists. Allows reflected tables to be
        # applied to models by name.
        if key in cls.metadata.tables:
            return sa.Table(*args, **kwargs)

        # If a primary key is found, create a table for joined-table inheritance.
        for arg in args:
            if (isinstance(arg, sa.Column) and arg.primary_key) or isinstance(
                arg, sa.PrimaryKeyConstraint
            ):
                return sa.Table(*args, **kwargs)

        # If no base classes define a table, return one that's missing a primary key
        # so SQLAlchemy shows the correct error.
        for base in cls.__mro__[1:-1]:
            if "__table__" in base.__dict__:
                break
        else:
            return sa.Table(*args, **kwargs)

        # Single-table inheritance, use the parent table name. __init__ will unset
        # __table__ based on this.
        if "__tablename__" in cls.__dict__:
            del cls.__tablename__

        return None
```
[ ] pallets-eco--flask-wtf--exempt
https://github.com/pallets-eco/flask-wtf/blob/f7259e91dab7efac8b33c9f86cb86f16f90207a1/./src/flask_wtf/csrf.py#L277-L304
```
    def exempt(self, view):
        """Mark a view or blueprint to be excluded from CSRF protection.

        ::

            @app.route('/some-view', methods=['POST'])
            @csrf.exempt
            def some_view():
                ...

        ::

            bp = Blueprint(...)
            csrf.exempt(bp)

        """

        if isinstance(view, Blueprint):
            self._exempt_blueprints.add(view)
            return view

        if isinstance(view, str):
            view_location = view
        else:
            view_location = ".".join((view.__module__, view.__name__))

        self._exempt_views.add(view_location)
        return view
```
[ ] pallets-eco--flask-wtf--hidden_tag
https://github.com/pallets-eco/flask-wtf/blob/f7259e91dab7efac8b33c9f86cb86f16f90207a1/./src/flask_wtf/form.py#L88-L119
```
    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, str):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup("\n".join(str(f) for f in hidden_fields(fields or self)))
```
[ ] pgjdbc--r2dbc-postgresql--isValid
https://github.com/pgjdbc/r2dbc-postgresql/blob/0947ac877a38f9af26e036dcb31faec6a94abe26/./src/main/java/io/r2dbc/postgresql/codec/PostgresqlObjectId.java#L458-L472
```
    /**
     * Returns if the {@code objectId} is a known and valid {@code objectId}.
     *
     * @param objectId the object id to match
     * @return {@code true} if the {@code objectId} is a valid and known (static) objectId;{@code false} otherwise.
     */
    public static boolean isValid(int objectId) {

        if (objectId >= 0 && objectId < OID_CACHE_SIZE) {
            PostgresqlObjectId oid = CACHE[objectId];
            return oid != null;
        }

        return false;
    }
```
[ ] pygfx--wgpu-py--__init__
https://github.com/pygfx/wgpu-py/blob/2845a5193d4e52ce64245259dcf2b3d18b83ca3c/./wgpu/_async.py#L87-L122
```
    def __init__(
        self,
        title: str,
        handler: Callable | None,
        *,
        loop: LoopInterface | None = None,
        poller: Callable | None = None,
        keepalive: object = None,
    ):
        """
        Arguments:
            title (str): The title of this promise, mostly for debugging purposes.
            handler (callable, optional): The function to turn promise input into the result. If None,
                the result will simply be the input.
            loop (LoopInterface, optional): A loop object that at least has a ``call_soon()`` method.
                If not given, this promise does not support .then() or pronise-chaining.
            poller (callable, optional): A function to call on a regular interval to poll internal systems
               (most likely the wgpu backend).
            keepalive (object, optional): Pass any data via this arg who's lifetime must be bound to the
                resolving of this prommise.

        """
        self._title = str(title)  # title for debugging
        self._handler = handler  # function to turn input into the result

        self._loop = loop  # Event loop instance, can be None
        self._poller = poller  # call to poll (process events)
        self._keepalive = keepalive  # just to keep something alive

        self._state = "pending"  # "pending", "pending-rejected", "pending-fulfilled", "rejected", "fulfilled"
        self._value = None  # The incoming value, final value, or error
        self._event = None  # AsyncEvent for __await__
        self._lock = threading.RLock()  # Allow threads to set the value
        self._done_callbacks = []
        self._error_callbacks = []
        self._UNRESOLVED.add(self)
```
[ ] pygfx--wgpu-py--dict_to_table
https://github.com/pygfx/wgpu-py/blob/2845a5193d4e52ce64245259dcf2b3d18b83ca3c/./wgpu/_diagnostics.py#L249-L287
```
def dict_to_table(d, header, header_offset=0):
    """Convert a dict data structure to a table (a list of lists of strings).
    The keys form the first entry of the row. Values that are dicts recurse.
    """

    ncols = len(header)
    rows = []

    for row_title, values in d.items():
        if row_title == "total" and row_title == list(d.keys())[-1]:
            rows.append([""] * ncols)
        row = [row_title + ":" if row_title else ""]
        rows.append(row)
        for i in range(header_offset + 1, len(header)):
            key = header[i]
            val = values.get(key, None)
            if val is None:
                row.append("")
            elif isinstance(val, str):
                row.append(val)
            elif isinstance(val, bool):
                row.append("✓" if val else "-")
            elif isinstance(val, int):
                row.append(int_repr(val))
            elif isinstance(val, float):
                row.append(f"{val:.6g}")
            elif isinstance(val, dict):
                subrows = dict_to_table(val, header, i)
                if len(subrows) == 0:
                    row += [""] * (ncols - i)
                else:
                    row += subrows[0]
                    extrarows = [[""] * i + subrow for subrow in subrows[1:]]
                    rows.extend(extrarows)
                break  # header items are consumed by the sub
            else:  # no-cover
                raise TypeError(f"Unexpected table value: {val}")

    return rows
```
[ ] pypyr--pypyr--__init__-4
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/formatting.py#L29-L48
```
    def __init__(self, format_spec):
        """Parse format_spec for recursion specifier.

        Args:
            format_spec (str): format specification parsed from string
                               formatting expression. Likely from Formatter's
                               .parse method.
        """
        recursion_spec = format_spec[:2]
        self.has_recursed = False
        self.is_set = False
        self.is_recursive = False
        self.is_flat = False

        if recursion_spec == 'rf':
            self.is_set = self.is_recursive = True
        elif recursion_spec == 'ff':
            self.is_set = self.is_flat = True

        self.format_spec = format_spec[2:] if self.is_set else format_spec
```
[ ] pypyr--pypyr--__init__-5
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/pipeline.py#L76-L119
```
    def __init__(self,
                 name: str,
                 context_args: list[str] | None = None,
                 parse_input: bool | None = True,
                 loader: str | None = None,
                 groups: list[str] | None = None,
                 success_group: str | None = None,
                 failure_group: str | None = None,
                 py_dir: str | bytes | PathLike | None = None) -> None:
        """Initialize a Pipeline.

        Args:
            name (str): Name of pipeline, sans .yaml at end.
            context_args (list[str]): All the input arguments after the
                pipeline name from cli.
            parse_input (bool): Default True. Run context_parser in pipeline.
            loader (str): Absolute name of pipeline loader module.
                        If not specified will use pypyr.loaders.file.
            groups (list[str]): Step-group names to run in pipeline.
                                Default if not set is ['steps'].
            success_group (str): Step-group name to run on success completion.
                                Default if not set is on_success.
            failure_group (str: Step-group name to run on pipeline failure.
                                Default if not set is on_failure.
            py_dir (Path-like): Custom python modules resolve from this dir.

        Returns:
            None
        """
        self.name = name
        self.context_args = context_args
        self.parse_input = parse_input
        self.loader = loader
        self.groups = groups
        self.success_group = success_group
        self.failure_group = failure_group
        self.py_dir = py_dir

        # initialize here, but use later
        # not using a classmethod fromLoader factory style thing coz PipeDef
        # AND StepsRunner depend on having a context object, which is subject
        # to logic only called later in obj life-time in load_and_run_pipeline.
        self.pipeline_definition = None
        self.steps_runner = None
```
[ ] pypyr--pypyr--__init__
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/dsl.py#L274-L331
```
    def __init__(self, step):
        """Initialize the class. No duh, huh?.

        You can happily expect the initializer to initialize all
        member attributes.

        Args:
            step: a string or a dict. This is the actual step as it exists in
                  the pipeline yaml - which is to say it can just be a string
                  for a simple step, or a dict for a complex step.
        """
        logger.debug("starting")

        # defaults for decorators
        self.description = None
        self.foreach_items = None
        self.in_parameters = None
        self.retry_decorator = None
        self.line_no = None
        self.line_col = None
        self.run_me = True
        self.skip_me = False
        self.swallow_me = False
        self.name = None
        self.while_decorator = None
        self.on_error = None

        try:
            if isinstance(step, dict):
                self._init_from_dict(step)
            else:
                # of course, it might not be a string. in line with duck
                # typing, beg forgiveness later. as long as it loads
                # the module, happy days.
                logger.debug("%s is a simple string.", step)
                self.name = step

            self.run_step_function = step_cache.get_step(self.name)
        except Exception:
            # Exceptions could also happened on the step init phase
            # (ModuleNotFound, KeyError, etc..),
            # put exception handler here because of that.
            # also handle case with missing step name
            name = f" {self.name}" if self.name else ""

            if self.line_no:
                logger.error(
                    "Error at pipeline step%s yaml line: "
                    "%d, col: %d",
                    name, self.line_no, self.line_col
                )
            else:
                logger.error(
                    "Error at pipeline step%s", name
                )
            raise

        logger.debug("done")
```
[ ] pypyr--pypyr--clear_pipes
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/cache/loadercache.py#L156-L174
```
    def clear_pipes(self, loader_name=None):
        """Clear the pipeline cache.

        Args:
            loader_name (str): Clear pipelines for this loader. If not
                specified, will iterate all loaders in the loaders cache and
                clear each of their pipelines.
        """
        if loader_name:
            loader = self._cache.get(loader_name, None)
            if loader:
                loader.clear()
            else:
                logger.debug(
                    "%s not found in loader cache so there's nothing to clear",
                    loader_name)
        else:
            for _, loader in self._cache.items():
                loader.clear()
```
[ ] pypyr--pypyr--env_unset
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/steps/env.py#L134-L176
```
def env_unset(context):
    """Unset $ENVs.

    Context is a dictionary or dictionary-like. context is mandatory.

    context['env']['unset'] must exist. It's a list.
    List items are the names of the $ENV values to unset.

    For example, say input context is:
        key1: value1
        key2: value2
        key3: value3
        env:
            unset:
                MYVAR1
                MYVAR2

    This will result in the following $ENVs being unset:
    $MYVAR1
    $MYVAR2
    """
    unset = context.get_formatted_value(context['env'].get('unset', None))

    exists = False
    if unset:
        logger.debug("started")

        for env_var_name in unset:
            logger.debug("unsetting $%s", env_var_name)
            try:
                del os.environ[env_var_name]
            except KeyError:
                # If user is trying to get rid of the $ENV, if it doesn't
                # exist, no real point in throwing up an error that the thing
                # you're trying to be rid off isn't there anyway.
                logger.debug(
                    "$%s doesn't exist anyway. As you were.", env_var_name)

        logger.info("unset %d $ENVs.", len(unset))
        exists = True

        logger.debug("done")
    return exists
```
[ ] pypyr--pypyr--get_parsed_context
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/parser/argskwargs.py#L25-L65
```
def get_parsed_context(args: list[str] | None) -> Mapping:
    """Create dict from combination of args & kwargs passed from cli.

    This supports the style of args that makefile does, i.e

    $ pypyr pipeline-name arg1 arg2 key1=value1 key2-"value 2"

    args go to context key `argList`. key=value pairs become context dictionary
    elements at root.

    Args:
      args: list of string. Passed from command-line invocation where:
            $ pypyr pipelinename this is the context_arg
            This would result in args == ['this', 'is', 'the', 'context_arg']

    Returns:
      dict. This dict will initialize the context for the pipeline run.
            The dict will have key `argList` with empty list [] if no args
            passed.
    """
    logger.debug("starting")
    if not args:
        logger.debug(
            "pipeline invoked without context arg set. For this\n"
            "argskwargs parser you're looking for something like:\n"
            "pypyr pipelinename arg1 arg2 k1=v1 k2=\"v 2\""
        )
        return {ARG_LIST_KEY: []}
    arg_list = []
    out: dict[str, str | list] = {}
    for a in args:
        # 1st = is separator, subsequent = just taken as part of the value
        key, sep, value = a.partition('=')
        if sep:
            out[key] = value
        else:
            arg_list.append(a)

    out[ARG_LIST_KEY] = arg_list

    return out
```
[ ] pypyr--pypyr--keys_of_type_exist
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/context.py#L474-L507
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
[ ] pypyr--pypyr--pip_install_extras
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/venv.py#L212-L238
```
    def pip_install_extras(self, pip_args: str) -> None:
        """Run python -m pip install {pip_args} in venv.

        You can ONLY call this AFTER post_setup() has run, which in practice
        means you have to have called create().
        """
        logger.debug("installing extra dependencies for path %s",
                     self.context.env_dir)

        cmd = [self.context.env_exec_cmd, '-m', 'pip', 'install']
        if self.is_quiet:
            cmd.append('-q')

        # if input is a list already, no need to shlex split
        shlexed_deps = shlex.split(pip_args) if isinstance(pip_args,
                                                           str) else pip_args

        # each arg could contain a path, thus run expand on all args
        for i, v in enumerate(shlexed_deps):
            shlexed_deps[i] = os.path.expanduser(v)

        cmd.extend(shlexed_deps)

        logger.debug("running %s", cmd)
        subprocess.run(cmd, check=True)

        logger.debug("done")
```
[ ] pypyr--pypyr--tar_archive
https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/steps/tar.py#L105-L140
```
def tar_archive(context_tar):
    """Archive specified path to a tar archive.

    Args:
        context_tar: dictionary-like. context is mandatory.
            context['tar']['archive'] must exist. It's a dictionary.
            keys are the paths to archive.
            values are the destination output paths.

    Example:
        tar:
            archive:
                - in: path/to/dir
                  out: path/to/destination.tar.xs
                - in: another/my.file
                  out: ./my.tar.xs

        This will archive directory path/to/dir to path/to/destination.tar.xs,
        and also archive file another/my.file to ./my.tar.xs
    """
    logger.debug("start")

    mode = get_file_mode_for_writing(context_tar)

    for item in context_tar['archive']:
        # value is the destination tar. Allow string interpolation.
        destination = item['out']
        # key is the source to archive
        source = item['in']
        with tarfile.open(destination, mode) as archive_me:
            logger.debug("Archiving '%s' to '%s'", source, destination)

            archive_me.add(source, arcname='.')
            logger.info("Archived '%s' to '%s'", source, destination)

    logger.debug("end")
```
[ ] pytr-org--pytr--_parse_type_dependent_params
https://github.com/pytr-org/pytr/blob/fa4b88d312feb159a9e7c876a6757e5976db3daf/./pytr/event.py#L241-L267
```
    @classmethod
    def _parse_type_dependent_params(
        cls, event_type: Optional[EventType], event_dict: Dict[Any, Any]
    ) -> Tuple[Optional[str], Optional[float], Optional[float], Optional[float], Optional[float], Optional[str]]:
        """Parses the fees, isin, note, shares and taxes fields

        Args:
            event_type (EventType): _description_
            event_dict (Dict[Any, Any]): _description_

        Returns:
            Tuple[Optional[Union[str, float]]]]: fees, isin, note, shares, taxes
        """
        isin, shares, value, fees, taxes, note = (None,) * 6

        if isinstance(event_type, ConditionalEventType) or event_type is PPEventType.DIVIDEND:
            isin = cls._parse_isin(event_dict)
            shares, value, fees, taxes, note = cls._parse_shares_value_fees_taxes_note(event_dict)
        else:
            value = v if (v := event_dict.get("amount", {}).get("value", None)) is not None and v != 0.0 else None

            if event_type is PPEventType.INTEREST:
                taxes = cls._parse_taxes(event_dict)
            elif event_type in [PPEventType.DEPOSIT, PPEventType.REMOVAL]:
                note = cls._parse_card_note(event_dict)

        return isin, shares, value, fees, taxes, note
```
[ ] r2dbc--r2dbc-proxy--chompIfEndWith
https://github.com/r2dbc/r2dbc-proxy/blob/d5b65d19e718e085e14349e77754b2213a4745c6/./src/main/java/io/r2dbc/proxy/support/FormatterUtils.java#L32-L51
```
    /**
     * Remove the matching {@code String} from the end of the given {@code StringBuilder}
     *
     * @param sb {@code StringBuilder}
     * @param s  removing {@code String} from tail
     * @throws IllegalArgumentException if {@code sb} is {@code null}
     * @throws IllegalArgumentException if {@code s} is {@code null}
     */
    public static void chompIfEndWith(StringBuilder sb, String s) {
        Assert.requireNonNull(sb, "sb must not be null");
        Assert.requireNonNull(s, "s must not be null");

        if (sb.length() < s.length()) {
            return;
        }
        final int startIndex = sb.length() - s.length();
        if (sb.substring(startIndex, sb.length()).equals(s)) {
            sb.delete(startIndex, sb.length());
        }
    }
```
[ ] r2dbc--r2dbc-proxy--showAll
https://github.com/r2dbc/r2dbc-proxy/blob/d5b65d19e718e085e14349e77754b2213a4745c6/./src/main/java/io/r2dbc/proxy/support/QueryExecutionInfoFormatter.java#L313-L331
```
    /**
     * Create a {@link QueryExecutionInfoFormatter} which writes out all attributes on {@link QueryExecutionInfo}.
     *
     * @return a formatter
     */
    public static QueryExecutionInfoFormatter showAll() {
        QueryExecutionInfoFormatter formatter = new QueryExecutionInfoFormatter();
        formatter.addConsumer(formatter.onThread);
        formatter.addConsumer(formatter.onConnection);
        formatter.addConsumer(formatter.onTransactionInfo);
        formatter.addConsumer(formatter.onSuccess);
        formatter.addConsumer(formatter.onTime);
        formatter.addConsumer(formatter.onType);
        formatter.addConsumer(formatter.onBatchSize);
        formatter.addConsumer(formatter.onBindingsSize);
        formatter.addConsumer(formatter.onQuery);
        formatter.addConsumer(formatter.onBindings);
        return formatter;
    }
```
[ ] ralscha--extdirectspring--addErrors-3
https://github.com/ralscha/extdirectspring/blob/2ff60f87631de56c27badca1ff9a173990832296/./src/main/java/ch/ralscha/extdirectspring/bean/ExtDirectFormPostResult.java#L183-L209
```
	/**
	 * Adds multiple error messages to a specific field. Does not overwrite already
	 * existing errors.
	 * @param field the name of the field
	 * @param errors a collection of error messages
	 */
	@SuppressWarnings("unchecked")
	public void addErrors(String field, List<String> errors) {
		Assert.notNull(field, "field must not be null");
		Assert.notNull(errors, "field must not be null");

		// do not overwrite existing errors
		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY);
		if (errorMap == null) {
			errorMap = new HashMap<>();
			addResultProperty(ERRORS_PROPERTY, errorMap);
		}

		List<String> fieldErrors = errorMap.get(field);
		if (fieldErrors == null) {
			fieldErrors = new ArrayList<>();
			errorMap.put(field, fieldErrors);
		}
		fieldErrors.addAll(errors);

		addResultProperty(SUCCESS_PROPERTY, Boolean.FALSE);
	}
```
[ ] ralscha--extdirectspring--equal
https://github.com/ralscha/extdirectspring/blob/2ff60f87631de56c27badca1ff9a173990832296/./src/main/java/ch/ralscha/extdirectspring/util/ExtDirectSpringUtil.java#L57-L65
```
	/**
	 * Checks if two objects are equal. Returns true if both objects are null
	 * @param a object one
	 * @param b object two
	 * @return true if objects are equal
	 */
	public static boolean equal(Object a, Object b) {
		return a == b || a != null && a.equals(b);
	}
```
[ ] ralscha--extdirectspring--handleCacheableResponse
https://github.com/ralscha/extdirectspring/blob/2ff60f87631de56c27badca1ff9a173990832296/./src/main/java/ch/ralscha/extdirectspring/util/ExtDirectSpringUtil.java#L155-L186
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, 6);

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		response.setContentLength(data.length);

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
[ ] ralscha--extdirectspring--isMultipart
https://github.com/ralscha/extdirectspring/blob/2ff60f87631de56c27badca1ff9a173990832296/./src/main/java/ch/ralscha/extdirectspring/util/ExtDirectSpringUtil.java#L67-L78
```
	/**
	 * Checks if the request is a multipart request
	 * @param request the HTTP servlet request
	 * @return true if request is a Multipart request (file upload)
	 */
	public static boolean isMultipart(HttpServletRequest request) {
		if (!"post".equals(request.getMethod().toLowerCase())) {
			return false;
		}
		String contentType = request.getContentType();
		return contentType != null && contentType.toLowerCase().startsWith("multipart/");
	}
```
[ ] restfb--restfb--cleanString
https://github.com/restfb/restfb/blob/9a98b76187b276a824fcd9109da988c2cc7c970a/./src/main/java/com/restfb/JsonHelper.java#L170-L183
```
  /**
   * removes starting and ending double quote from an input String
   * 
   * @param jsonInput
   *          input JSON string
   * @return the cleaned input string without leading and ending double quote
   */
  public String cleanString(String jsonInput) {
    if (jsonInput.length() > 1 && jsonInput.startsWith("\"") && jsonInput.endsWith("\"")) {
      return jsonInput.substring(1, jsonInput.length() - 1);
    }

    return jsonInput;
  }
```
[ ] restfb--restfb--extractParametersFromUrl
https://github.com/restfb/restfb/blob/9a98b76187b276a824fcd9109da988c2cc7c970a/./src/main/java/com/restfb/util/UrlUtils.java#L119-L149
```
  /**
   * For the given {@code url}, extract a mapping of query string parameter names to values.
   * <p>
   * Adapted from an implementation by BalusC and dfrankow, available at
   * <a href="http://stackoverflow.com/questions/1667278/parsing-query-strings-in-java">
   * http://stackoverflow.com/questions/1667278/parsing-query-strings-in-java</a>.
   *
   * @param url
   *          The URL from which parameters are extracted.
   * @return A mapping of query string parameter names to values. If {@code url} is {@code null}, an empty {@code Map}
   *         is returned.
   * @throws IllegalStateException
   *           If unable to URL-decode because the JVM doesn't support {@link StandardCharsets#UTF_8}.
   */
  public static Map<String, List<String>> extractParametersFromUrl(String url) {
    if (url == null) {
      return emptyMap();
    }

    Map<String, List<String>> parameters = new HashMap<>();
    String[] urlParts = url.split("\\?");

    if (urlParts.length > 1) {
      String query = urlParts[1];
      parameters = Pattern.compile("&").splitAsStream(query) //
        .map(s -> Arrays.copyOf(s.split("="), 2))
        .collect(Collectors.groupingBy(s -> urlDecode(s[0]), Collectors.mapping(s -> urlDecode(s[1]), toList())));
    }

    return parameters;
  }
```
[ ] restfb--restfb--getEntities
https://github.com/restfb/restfb/blob/9a98b76187b276a824fcd9109da988c2cc7c970a/./src/main/lombok/com/restfb/types/webhook/messaging/NlpResult.java#L129-L146
```
  /**
   * returns a subset of the found entities.
   *
   * Only entities that are of type <code>T</code> are returned. T needs to extend the {@link BaseNlpEntity}.
   *
   * @param clazz
   *          the filter class
   * @return List of entites, only the filtered elements are returned.
   */
  public <T extends BaseNlpEntity> List<T> getEntities(Class<T> clazz) {
    List<BaseNlpEntity> resultList = new ArrayList<>();
    for (BaseNlpEntity item : getEntities()) {
      if (item.getClass().equals(clazz)) {
        resultList.add(item);
      }
    }
    return (List<T>) resultList;
  }
```
[ ] restfb--restfb--getItem
https://github.com/restfb/restfb/blob/9a98b76187b276a824fcd9109da988c2cc7c970a/./src/main/lombok/com/restfb/types/webhook/messaging/MessagingItem.java#L144-L214
```
  /**
   * generic access to the inner item.
   * 
   * depending on the inner elements the corresponding element is returned. So you can get an {@link OptinItem},
   * {@link PostbackItem}, {@link DeliveryItem}, {@link AccountLinkingItem} or {@link MessageItem}
   * 
   * @return the inner item.
   */
  public InnerMessagingItem getItem() {
    if (optin != null) {
      return optin;
    }

    if (postback != null) {
      return postback;
    }

    if (delivery != null) {
      return delivery;
    }

    if (read != null) {
      return read;
    }

    if (accountLinking != null) {
      return accountLinking;
    }

    if (message != null) {
      return message;
    }

    if (checkoutUpdate != null) {
      return checkoutUpdate;
    }

    if (payment != null) {
      return payment;
    }

    if (referral != null) {
      return referral;
    }

    if (policyEnforcement != null) {
      return policyEnforcement;
    }

    if (passThreadControl != null) {
      return passThreadControl;
    }

    if (takeThreadControl != null) {
      return takeThreadControl;
    }

    if (requestThreadControl != null) {
      return requestThreadControl;
    }

    if (appRoles != null) {
      return appRoles;
    }

    if (reaction != null) {
      return reaction;
    }

    return null;
  }
```
[ ] restfb--restfb--toDateFromShortFormat
https://github.com/restfb/restfb/blob/9a98b76187b276a824fcd9109da988c2cc7c970a/./src/main/java/com/restfb/util/DateUtils.java#L125-L146
```
  /**
   * Returns a Java representation of a Facebook "short" {@code date} string.
   * 
   * @param date
   *          Facebook {@code date} string.
   * @return Java date representation of the given Facebook "short" {@code date} string or {@code null} if {@code date}
   *         is {@code null} or invalid.
   */
  public static Date toDateFromShortFormat(String date) {
    if (isNull(date)) {
      return null;
    }

    Date parsedDate = toDateWithFormatString(date, FACEBOOK_SHORT_DATE_FORMAT);

    // Fall back to variant if initial parse fails
    if (isNull(parsedDate)) {
      parsedDate = toDateWithFormatString(date, FACEBOOK_ALTERNATE_SHORT_DATE_FORMAT);
    }

    return parsedDate;
  }
```
[ ] revelc--impsort-maven-plugin--determineLineEnding
https://github.com/revelc/impsort-maven-plugin/blob/c1910f7dab00f6f7cc654501459442658a74fdd7/./src/main/java/net/revelc/code/impsort/LineEnding.java#L35-L69
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
[ ] roboflow--maestro--parse_roboflow_identifier
https://github.com/roboflow/maestro/blob/f394fce0b2c2fe98b3f457ad5abb61a9c7e88c7b/./maestro/trainer/common/datasets/roboflow.py#L10-L41
```
def parse_roboflow_identifier(identifier: str) -> Optional[tuple[str, str, Optional[int]]]:
    """
    Parses a Roboflow identifier and extracts the workspace, project, and optional dataset version.

    Args:
        identifier (str): The Roboflow identifier, which can be a full URL or a partial identifier string.

    Returns:
        Optional[tuple[str, str, Optional[int]]]: A tuple in the form of (workspace_id, project_id, dataset_version)
            if the identifier is valid; otherwise, None.
    """
    identifier_no_protocol = re.sub(r"^https?://", "", identifier.strip())
    domain_pattern = r"^(?:[^/]*roboflow\.com)/?"
    identifier_no_domain = re.sub(domain_pattern, "", identifier_no_protocol)
    tokens = [segment for segment in identifier_no_domain.split("/") if segment]

    if len(tokens) < 2:
        return None

    workspace = tokens[0]
    project = tokens[1]
    version = None

    if len(tokens) > 3:
        return None
    elif len(tokens) == 3:
        try:
            version = int(tokens[2])
        except ValueError:
            return None

    return workspace, project, version
```
[ ] romankh3--image-comparison--containsPoint
https://github.com/romankh3/image-comparison/blob/0e9c63792af31dac63b439554dcc0d35c34e0b78/./src/main/java/com/github/romankh3/image/comparison/model/Rectangle.java#L152-L160
```
    /**
     * Check if the provided {@link Point} contains in the {@link Rectangle}.
     *
     * @param point provided {@link Point}.
     * @return {@code true} if provided {@link Point} contains, {@code false} - otherwise.
     */
    boolean containsPoint(Point point) {
        return  point.x >= minPoint.x && point.x<= maxPoint.x && point.y >= minPoint.y && point.y <= maxPoint.y;
    }
```
[ ] sashirestela--simple-openai--executeAll
https://github.com/sashirestela/simple-openai/blob/fe2438bde0895e2abff81d47f154211704ebfc61/./src/main/java/io/github/sashirestela/openai/common/function/FunctionExecutor.java#L95-L115
```
    /**
     * Run the 'execute()' method for a list of FunctionDefs.
     * 
     * @param <R>            Specific type to gather the result. ToolMessage for ChatCompletion or
     *                       ToolOutput for Assistants.
     * @param toolCalls      Response from the model to call functions.
     * @param toolOutputItem BiFunction with two arguments: 'toolCallId' and 'result'. Returns a new R
     *                       object with those arguments.
     * @return List of R objects.
     */
    public <R> List<R> executeAll(List<ToolCall> toolCalls, BiFunction<String, String, R> toolOutputItem) {
        List<R> toolOutputs = new ArrayList<>();
        for (var toolCall : toolCalls) {
            if (toolCall.getFunction() != null) {
                var result = execute(toolCall.getFunction());
                var item = toolOutputItem.apply(toolCall.getId(), result.toString());
                toolOutputs.add(item);
            }
        }
        return toolOutputs;
    }
```
[ ] scrapinghub--scrapyrt--handle_error
https://github.com/scrapinghub/scrapyrt/blob/edc41140a6c82ecfe9d8e195e7bddb7ec3a9cc9a/./scrapyrt/resources.py#L50-L78
```
    def handle_error(self, exception_or_failure, request):
        """Override this method to add custom exception handling.

        :param request: twisted.web.server.Request
        :param exception_or_failure: Exception or
            twisted.python.failure.Failure
        :return: dict which will be converted to JSON error response

        """
        failure = None
        if isinstance(exception_or_failure, Exception):
            exception: BaseException = exception_or_failure
        else:
            assert isinstance(exception_or_failure, Failure)
            assert exception_or_failure.value is not None
            exception = exception_or_failure.value
            failure = exception_or_failure
        if request.code == 200:  # noqa: PLR2004
            # Default code - means that error wasn't handled
            if isinstance(exception, UnsupportedMethod):
                request.setResponseCode(405)
            elif isinstance(exception, Error):
                code = int(exception.status)
                request.setResponseCode(code)
            else:
                request.setResponseCode(500)
            if request.code == 500:  # noqa: PLR2004
                log.err(failure)
        return self.format_error_response(exception, request)
```
[ ] sherlock-project--sherlock--remove_nsfw_sites
https://github.com/sherlock-project/sherlock/blob/339634f7bc370517b06f960b464b10935bb829fb/./sherlock_project/sites.py#L213-L229
```
    def remove_nsfw_sites(self, do_not_remove: list = []):
        """
        Remove NSFW sites from the sites, if isNSFW flag is true for site

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        None
        """
        sites = {}
        do_not_remove = [site.casefold() for site in do_not_remove]
        for site in self.sites:
            if self.sites[site].is_nsfw and site.casefold() not in do_not_remove:
                continue
            sites[site] = self.sites[site]
        self.sites =  sites
```
[ ] siboehm--lleaves--ndarray_to_ptr
https://github.com/siboehm/lleaves/blob/5e977601aec086833f578d03885ca7e6eb6b3499/./lleaves/data_processing.py#L96-L112
```
def ndarray_to_ptr(data: np.ndarray, use_fp64: bool = True):
    """
    Takes a 2D numpy array, converts it to either float64 or float32 depending on the `use_fp64` flag,
    and returns a pointer to the data.

    :param data: 2D numpy array. Copying is avoided if possible.
    :param use_fp64: Bool. Casting to float64 if True, otherwise float32.
    :return: pointer to 1D array of type float64 if `use_fp64` is True, otherwise float32.
    """
    # ravel makes sure we get a contiguous array in memory and not some strided View
    data = data.astype(
        np.float64 if use_fp64 else np.float32,
        copy=False,
        casting="same_kind",
    ).ravel()
    ptr = data.ctypes.data_as(POINTER(c_double if use_fp64 else c_float))
    return ptr
```
[ ] spotify--futures-extra--grabJob
https://github.com/spotify/futures-extra/blob/f12c25cb77286c88c11777e609baf3e36310af9d/./src/main/java/com/spotify/futures/ConcurrencyLimiter.java#L145-L163
```
  /**
   * Return a {@code Job} with acquired permit, {@code null} otherwise.
   *
   * <p>Does one of two things: 1) return a job and acquire a permit from the semaphore 2) return
   * null and does not acquire a permit from the semaphore
   */
  private Job<T> grabJob() {
    if (!limit.tryAcquire()) {
      return null;
    }

    final Job<T> job = queue.poll();
    if (job != null) {
      return job;
    }

    limit.release();
    return null;
  }
```
[ ] theskumar--python-dotenv--get_cli_string
https://github.com/theskumar/python-dotenv/blob/85f43295ccb2d15d13da370954e5b85079f4a56c/./src/dotenv/__init__.py#L12-L39
```
def get_cli_string(
    path: Optional[str] = None,
    action: Optional[str] = None,
    key: Optional[str] = None,
    value: Optional[str] = None,
    quote: Optional[str] = None,
):
    """Returns a string suitable for running as a shell script.

    Useful for converting a arguments passed to a fabric task
    to be passed to a `local` or `run` command.
    """
    command = ["dotenv"]
    if quote:
        command.append(f"-q {quote}")
    if path:
        command.append(f"-f {path}")
    if action:
        command.append(action)
        if key:
            command.append(key)
            if value:
                if " " in value:
                    command.append(f'"{value}"')
                else:
                    command.append(value)

    return " ".join(command).strip()
```
[ ] thombashi--pytablewriter--get_extensions
https://github.com/thombashi/pytablewriter/blob/5da77a0b64e15451aceed41350712425d95ead62/./pytablewriter/_factory.py#L230-L274
```
    @classmethod
    def get_extensions(cls) -> list[str]:
        """
        :return: Available file extensions.
        :rtype: list

        :Example:
            .. code:: python

                >>> import pytablewriter as ptw
                >>> for name in ptw.TableWriterFactory.get_extensions():
                ...     print(name)
                ...
                adoc
                asc
                asciidoc
                css
                csv
                htm
                html
                js
                json
                jsonl
                ldjson
                ltsv
                md
                ndjson
                py
                rst
                sqlite
                sqlite3
                tex
                toml
                tsv
                xls
                xlsx
                yml
        """

        file_extension_set = set()
        for table_format in TableFormat:
            for file_extension in table_format.file_extensions:
                file_extension_set.add(file_extension)

        return sorted(list(file_extension_set))
```
[ ] thombashi--pytablewriter--write_table-3
https://github.com/thombashi/pytablewriter/blob/5da77a0b64e15451aceed41350712425d95ead62/./pytablewriter/writer/text/_markdown.py#L128-L171
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table:
                self.write_null_line()
```
[x] tomdesair--tus-java-server--getFileName
https://github.com/tomdesair/tus-java-server/blob/1c4adf10e2ef29d86f94e572c35e7e22137ff3a0/./src/main/java/me/desair/tus/server/upload/UploadInfo.java#L321-L337
```
  /**
   * Try to guess the filename of the uploaded data. If we cannot guess the name we fall back to the
   * ID. <br>
   * NOTE: This is only a guess, there are no guarantees that the return value is correct
   *
   * @return A potential file name
   */
  public String getFileName() {
    Map<String, String> metadata = getMetadata();
    for (String fileNameKey : fileNameKeys) {
      if (metadata.containsKey(fileNameKey)) {
        return metadata.get(fileNameKey);
      }
    }

    return getId().toString();
  }
```
[ ] tomdesair--tus-java-server--getMetadata
https://github.com/tomdesair/tus-java-server/blob/1c4adf10e2ef29d86f94e572c35e7e22137ff3a0/./src/main/java/me/desair/tus/server/upload/UploadInfo.java#L99-L131
```
  /**
   * Get the decoded metadata map provided by the client based on the encoded Tus metadata string
   * received on creation of the upload. The encoded metadata string consists of one or more
   * comma-separated key-value pairs where the key is ASCII encoded and the value Base64 encoded.
   * The key and value MUST be separated by a space. See
   * https://tus.io/protocols/resumable-upload.html#upload-metadata
   *
   * @return The encoded metadata string as received from the client
   */
  public Map<String, String> getMetadata() {
    Map<String, String> metadata = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);
    for (String valuePair : splitToArray(encodedMetadata, ",")) {
      String[] keyValue = splitToArray(valuePair, "\\s");
      String key = null;
      String value = null;
      if (keyValue.length > 0) {
        key = StringUtils.trimToEmpty(keyValue[0]);

        // Skip any blank values
        int i = 1;
        while (keyValue.length > i && StringUtils.isBlank(keyValue[i])) {
          i++;
        }

        if (keyValue.length > i) {
          value = decode(keyValue[i]);
        }

        metadata.put(key, value);
      }
    }
    return metadata;
  }
```
[ ] tuneflow--tuneflow-py--greater_than
https://github.com/tuneflow/tuneflow-py/blob/b5736cba31843590cdfefd6dd9c748110d347f69/./src/tuneflow_py/utils.py#L63-L79
```
def greater_than(sorted_list: list, val, key: Callable | None = None, low: int | None = None, high: int | None = None):
    '''
    Returns the index of the first item in the array > val. This is the same as a successor query.
    '''
    low = low if low is not None else 0
    high = high if high is not None else len(sorted_list) - 1
    i = high + 1
    while low <= high:
        m = (low + high) >> 1
        x = sorted_list[m]
        p = (key(x) - key(val)) if key is not None else (x - val)
        if p > 0:
            i = m
            high = m - 1
        else:
            low = m + 1
    return i
```
[ ] tzaeschke--zoodb--readSchemaAll
https://github.com/tzaeschke/zoodb/blob/311c96bc6f9413762c54b4638c85a60558707aab/./src/org/zoodb/internal/server/DiskAccessOneFile.java#L167-L189
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
[ ] uncertainty-toolbox--uncertainty-toolbox--check_score
https://github.com/uncertainty-toolbox/uncertainty-toolbox/blob/6ea1fed6591923a95d49d8049a197e33d4d8092d/./uncertainty_toolbox/metrics_scoring_rule.py#L92-L142
```
def check_score(
    y_pred: np.ndarray,
    y_std: np.ndarray,
    y_true: np.ndarray,
    scaled: bool = True,
    start_q: float = 0.01,
    end_q: float = 0.99,
    resolution: int = 99,
) -> float:
    """The negatively oriented check score.

    Computes the negatively oriented check score for held out data (y_true)
    given predictive uncertainty with mean (y_pred) and standard-deviation (y_std).
    Each test point and each quantile is given equal weight in the overall score
    over the test set and list of quantiles.

    The score is computed by scanning over a sequence of quantiles of the predicted
    distributions, starting at (start_q) and ending at (end_q).

    Negatively oriented means a smaller value is more desirable.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_std: 1D array of the predicted standard deviations for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.
        scaled: Whether to scale the score by size of held out set.
        start_q: The lower bound of the quantiles to use for computation.
        end_q: The upper bound of the quantiles to use for computation.
        resolution: The number of quantiles to use for computation.

    Returns:
        The check score.
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_std, y_true)

    test_qs = np.linspace(start_q, end_q, resolution)

    check_list = []
    for q in test_qs:
        q_level = stats.norm.ppf(q, loc=y_pred, scale=y_std)  # pred quantile
        diff = q_level - y_true
        mask = (diff >= 0).astype(float) - q
        score_per_q = np.mean(mask * diff)
        check_list.append(score_per_q)
    check_score = np.sum(check_list)

    if scaled:
        check_score = check_score / len(check_list)

    return check_score
```
[ ] uncertainty-toolbox--uncertainty-toolbox--prediction_error_metrics
https://github.com/uncertainty-toolbox/uncertainty-toolbox/blob/6ea1fed6591923a95d49d8049a197e33d4d8092d/./uncertainty_toolbox/metrics_accuracy.py#L16-L52
```
def prediction_error_metrics(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> Dict[str, float]:
    """Get all prediction error metrics.

    Args:
        y_pred: 1D array of the predicted means for the held out dataset.
        y_true: 1D array of the true labels in the held out dataset.

    Returns:
        A dictionary with Mean average error ('mae'), Root mean squared
        error ('rmse'), Median absolute error ('mdae'),  Mean absolute
        relative percent difference ('marpd'), r^2 ('r2'), and Pearson's
        correlation coefficient ('corr').
    """
    # Check that input arrays are flat
    assert_is_flat_same_shape(y_pred, y_true)

    # Compute metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mdae = median_absolute_error(y_true, y_pred)
    residuals = y_true - y_pred
    marpd = np.abs(2 * residuals / (np.abs(y_pred) + np.abs(y_true))).mean() * 100
    r2 = r2_score(y_true, y_pred)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    prediction_metrics = {
        "mae": mae,
        "rmse": rmse,
        "mdae": mdae,
        "marpd": marpd,
        "r2": r2,
        "corr": corr,
    }

    return prediction_metrics
```
[ ] uncertainty-toolbox--uncertainty-toolbox--trapezoid_area
https://github.com/uncertainty-toolbox/uncertainty-toolbox/blob/6ea1fed6591923a95d49d8049a197e33d4d8092d/./uncertainty_toolbox/utils.py#L48-L105
```
def trapezoid_area(
    xl: np.ndarray,
    al: np.ndarray,
    bl: np.ndarray,
    xr: np.ndarray,
    ar: np.ndarray,
    br: np.ndarray,
    absolute: bool = True,
) -> Numeric:
    """
    Calculate the area of a vertical-sided trapezoid, formed connecting the following points:
        (xl, al) - (xl, bl) - (xr, br) - (xr, ar) - (xl, al)

    This function considers the case that the edges of the trapezoid might cross,
    and explicitly accounts for this.

    Args:
        xl: The x coordinate of the left-hand points of the trapezoid
        al: The y coordinate of the first left-hand point of the trapezoid
        bl: The y coordinate of the second left-hand point of the trapezoid
        xr: The x coordinate of the right-hand points of the trapezoid
        ar: The y coordinate of the first right-hand point of the trapezoid
        br: The y coordinate of the second right-hand point of the trapezoid
        absolute: Whether to calculate the absolute area, or allow a negative area (e.g. if a and b are swapped)

    Returns: The area of the given trapezoid.

    """

    # Differences
    dl = bl - al
    dr = br - ar

    # The ordering is the same for both iff they do not cross.
    cross = dl * dr < 0

    # Treat the degenerate case as a trapezoid
    cross = cross * (1 - ((dl == 0) * (dr == 0)))

    # trapezoid for non-crossing lines
    area_trapezoid = (xr - xl) * 0.5 * ((bl - al) + (br - ar))
    if absolute:
        area_trapezoid = np.abs(area_trapezoid)

    # Hourglass for crossing lines.
    # NaNs should only appear in the degenerate and parallel cases.
    # Those NaNs won't get through the final multiplication so it's ok.
    with np.errstate(divide="ignore", invalid="ignore"):
        x_intersect = intersection((xl, bl), (xr, br), (xl, al), (xr, ar))[0]
    tl_area = 0.5 * (bl - al) * (x_intersect - xl)
    tr_area = 0.5 * (br - ar) * (xr - x_intersect)
    if absolute:
        area_hourglass = np.abs(tl_area) + np.abs(tr_area)
    else:
        area_hourglass = tl_area + tr_area

    # The nan_to_num function allows us to do 0 * nan = 0
    return (1 - cross) * area_trapezoid + cross * np.nan_to_num(area_hourglass)
```
[ ] wangguanquan--eec--calculateFinalLumValue
https://github.com/wangguanquan/eec/blob/43cbda4ee4e09bf9988e033f4e4ac8cc3b108af4/./src/main/java/org/ttzero/excel/entity/style/HlsColor.java#L109-L128
```
    /**
     * If tint is supplied, then it is applied to the value of the color to determine the final color applied.
     * <p>
     * The tint value is stored as a double from {@code -1.0 .. 1.0}, where {@code -1.0} means {@code 100%} darken
     * and {@code 1.0} means {@code 100%} lighten. Also, {@code 0.0} means no change.
     * <p>
     * In loading the value, it is converted to HLS where HLS values are (0..HLSMAX), where HLSMAX is currently 255.
     * <p>
     * Referer: <a href="https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.spreadsheet.color?view=openxml-2.8.1">Tint</a>
     *
     * @param tint Specifies the tint value applied to the color.
     * @param lum Luminance part
     * @return calculate tint Luminance
     */
    public static float calculateFinalLumValue(Double tint, float lum) {
        if (tint == null) return lum;
        if (tint < 0) lum = (float) (lum * (1 + tint));
        else lum = (float) (lum * (1 - tint) + (255 - 255 * (1 - tint)));
        return lum;
    }
```
[ ] wangguanquan--eec--listDeclaredFields
https://github.com/wangguanquan/eec/blob/43cbda4ee4e09bf9988e033f4e4ac8cc3b108af4/./src/main/java/org/ttzero/excel/util/ReflectUtil.java#L59-L86
```
    /**
     * List all declared fields that contains all supper class
     *
     * @param beanClass The bean class to be analyzed.
     * @param stopClass The base class at which to stop the analysis.  Any
     *                  methods/properties/events in the stopClass or in its base classes
     *                  will be ignored in the analysis.
     * @return all declared fields
     */
    public static Field[] listDeclaredFields(Class<?> beanClass, Class<?> stopClass) {
        Field[] fields = beanClass.getDeclaredFields();
        int i = fields.length, last = 0;
        for (; (beanClass = beanClass.getSuperclass()) != stopClass && beanClass != null; ) {
            Field[] subFields = beanClass.getDeclaredFields();
            if (subFields.length > 0) {
                if (subFields.length > last) {
                    Field[] tmp = new Field[fields.length + subFields.length];
                    System.arraycopy(fields, 0, tmp, 0, i);
                    fields = tmp;
                    last = tmp.length - i;
                }
                System.arraycopy(subFields, 0, fields, i, subFields.length);
                i += subFields.length;
                last -= subFields.length;
            }
        }
        return fields;
    }
```
[ ] wangguanquan--eec--mightContain
https://github.com/wangguanquan/eec/blob/43cbda4ee4e09bf9988e033f4e4ac8cc3b108af4/./src/main/java/org/ttzero/excel/hash/StringBloomFilter.java#L84-L103
```
        /**
         * Queries {@code numHashFunctions} bits of the given bit array, by hashing a user element;
         * returns {@code true} if and only if all selected bits are set.
         */
        public boolean mightContain(String object, Charset charset, int numHashFunctions, LockFreeBitArray bits) {
            long bitSize = bits.bitSize();
            byte[] bytes = hasher.clear().putBytes(object.getBytes(charset)).hash();
            long hash1 = fromBytes(bytes[7], bytes[6], bytes[5], bytes[4], bytes[3], bytes[2], bytes[1], bytes[0]);
            long hash2 = fromBytes(bytes[15], bytes[14], bytes[13], bytes[12], bytes[11], bytes[10], bytes[9], bytes[8]);

            long combinedHash = hash1;
            for (int i = 0; i < numHashFunctions; i++) {
                // Make the combined hash positive and indexable
                if (!bits.get((combinedHash & Long.MAX_VALUE) % bitSize)) {
                    return false;
                }
                combinedHash += hash2;
            }
            return true;
        }
```
[ ] wangguanquan--eec--write-3
https://github.com/wangguanquan/eec/blob/43cbda4ee4e09bf9988e033f4e4ac8cc3b108af4/./src/main/java/org/ttzero/excel/util/CSVUtil.java#L1147-L1206
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
[ ] wangguanquan--eec--writeWithBom
https://github.com/wangguanquan/eec/blob/43cbda4ee4e09bf9988e033f4e4ac8cc3b108af4/./src/main/java/org/ttzero/excel/util/CSVUtil.java#L1006-L1019
```
        /**
         * Write csv bytes with BOM
         *
         * <p>Note: This property must be set before writing, otherwise it will be ignored</p>
         *
         * @return current writer
         */
        public Writer writeWithBom() {
            if (offset == 0 && i == 0 && column == 0) {
                // Write UTF BOM
                cb[offset++] = '\uFEFF';
            }
            return this;
        }
```
[ ] wbopan--moffee--chunk
https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/compositor.py#L115-L150
```
    @property
    def chunk(self) -> Chunk:
        """
        Split raw_md into chunk tree
        Chunk tree branches when in-page divider is met.
        - adjacent "<->"s create chunk with horizontal direction
        - adjacent "===" create chunk with vertical direction
        "===" possesses higher priority than "<->"

        :return: Root of the chunk tree
        """

        def split_by_div(text, type) -> List[Chunk]:
            strs = [""]
            current_escaped = False
            for line in text.split("\n"):
                if line.strip().startswith("```"):
                    current_escaped = not current_escaped
                if is_divider(line, type) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] += line + "\n"
            return [Chunk(paragraph=s) for s in strs]

        # collect "==="
        vchunks = split_by_div(self.raw_md, "=")
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
[ ] wbopan--moffee--copy_assets
https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/utils/file_helper.py#L87-L147
```
def copy_assets(document: str, target_dir: str) -> str:
    """
    Copy all asset resources in an HTML document to target_dir, then update URLs to target_dir/uuid_originalname.ext
    Handles encoded URLs.

    :param document: HTML document to process
    :param target_dir: Target directory
    :return: Updated document with URLs redirected
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    soup = BeautifulSoup(document, "html.parser")

    # Dictionary to store original path to new path mapping
    path_mapping = {}

    # Tags and attributes to check for URLs
    tag_attr_pairs = [
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
        ("a", "href"),
    ]

    for tag, attr in tag_attr_pairs:
        for element in soup.find_all(tag):
            if element.has_attr(attr):
                original_path = element[attr]

                # Decode the URL
                decoded_path = unquote(original_path)

                # Skip if it's an external URL
                if urlparse(decoded_path).scheme:
                    continue

                # Convert to absolute path if it's relative
                absolute_path = os.path.abspath(decoded_path)

                # Skip if it's not a file
                if not os.path.isfile(absolute_path):
                    continue

                if original_path not in path_mapping:
                    # Generate a new filename
                    original_filename = os.path.basename(absolute_path)
                    name, ext = os.path.splitext(original_filename)
                    new_filename = f"{str(uuid.uuid4())[:8]}_{name}{ext}"
                    new_path = os.path.join(target_dir, new_filename)

                    # Copy the file
                    shutil.copy2(absolute_path, new_path)

                    # Store the mapping
                    path_mapping[original_path] = new_path

                # Update the attribute with the new path
                element[attr] = quote(path_mapping[original_path])

    return str(soup)
```
[ ] wbopan--moffee--parse_frontmatter
https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/compositor.py#L166-L198
```
def parse_frontmatter(document: str) -> Tuple[str, PageOption]:
    """
    Parse the YAML front matter in a given markdown document.

    :param document: Input markdown document as a string.
    :return: A tuple containing the document with front matter removed and the PageOption.
    """
    document = document.strip()
    front_matter = ""
    content = document

    # Check if the document starts with '---'
    if document.startswith("---"):
        parts = document.split("---", 2)
        if len(parts) >= 3:
            front_matter = parts[1].strip()
            content = parts[2].strip()

    # Parse YAML front matter
    try:
        yaml_data = yaml.safe_load(front_matter) if front_matter else {}
    except yaml.YAMLError:
        yaml_data = {}

    # Create PageOption from YAML data
    option = PageOption()
    for field in fields(option):
        name = field.name
        if name in yaml_data:
            setattr(option, name, yaml_data.pop(name))
    option.styles = yaml_data

    return content, option
```
[ ] wbopan--moffee--redirect_paths
https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/utils/file_helper.py#L25-L84
```
def redirect_paths(document: str, document_path: str, resource_dir: str = ".") -> str:
    """
    Redirect all relative paths in a document to absolute paths with some guessing.
    Following possible base paths will be tried:
    - The original path itself maybe a valid absolute url (Absolute path or http)
    - The direct parent dir of the document
    - The resource dir (if it exists as an absolute path)
    - The resource dir relative to the document (Otherwise)

    :param document: HTML document string
    :param document_path: Path to the document
    :param resource_dir: Optional resource path
    :return: Document string with all urls redirected.
    """

    def is_absolute_url(url):
        return bool(urlparse(url).netloc) or (
            os.path.isabs(url) and os.path.exists(url)
        )

    def make_absolute(base, relative):
        return os.path.abspath(os.path.normpath(os.path.join(base, relative)))

    def redirect_url(url):
        if is_absolute_url(url):
            return url

        # Try different base paths to make the URL absolute
        base_paths = [
            os.path.dirname(document_path),
            os.path.abspath(resource_dir),
            os.path.join(os.path.dirname(document_path), resource_dir),
        ]

        for base in base_paths:
            absolute_url = make_absolute(base, url)
            if os.path.exists(absolute_url) or is_absolute_url(absolute_url):
                return absolute_url

        return url

    soup = BeautifulSoup(document, "html.parser")

    # Tags and attributes to check for URLs
    tag_attr_pairs = [
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
        ("a", "href"),
    ]

    for tag, attr in tag_attr_pairs:
        for element in soup.find_all(tag):
            if element.has_attr(attr):
                original_url = element[attr]
                decoded_url = unquote(original_url)
                redirected_url = redirect_url(decoded_url)
                element[attr] = redirected_url

    return str(soup)
```
[ ] wntrblm--nox--_find_pbs_python
https://github.com/wntrblm/nox/blob/38dea062a14355469fa44170ec64694b2c2d5e7f/./nox/virtualenv.py#L179-L191
```
def _find_pbs_python(implementation: str, version: str) -> str | None:
    """Check for an existing pbs-installer installation
    by default it creates dirs with this format:
    "pypy@3.8.16", "cpython@3.13.3" """
    executable = "python.exe" if _PLATFORM.startswith("win") else "bin/python"

    if NOX_PBS_PYTHONS.exists():
        for path in NOX_PBS_PYTHONS.iterdir():
            if path.is_dir() and path.name.startswith(f"{implementation}@{version}."):
                python_exe = path / executable
                if python_exe.exists():
                    return str(python_exe)
    return None
```
[ ] wntrblm--nox--filter_by_tags
https://github.com/wntrblm/nox/blob/38dea062a14355469fa44170ec64694b2c2d5e7f/./nox/manifest.py#L223-L230
```
    def filter_by_tags(self, tags: Iterable[str]) -> None:
        """Filter sessions by their tags.

        Args:
            tags (list[str]): A list of tags which session names
                are checked against.
        """
        self._queue = [x for x in self._queue if set(x.tags).intersection(tags)]
```
[ ] xjodoin--torpedoquery--and
https://github.com/xjodoin/torpedoquery/blob/09a3357b34f1e68b3715142c421507c2a38bdd96/./src/main/java/org/torpedoquery/jpa/Torpedo.java#L994-L1012
```
	/**
	 * Group expressions together in a single conjunction (A and B and C...)
	 *
	 * @param conditions a {@link java.lang.Iterable} object.
	 * @return OnGoingLogicalCondition
	 */
	public static OnGoingLogicalCondition and(Iterable<OnGoingLogicalCondition> conditions) {
		OnGoingLogicalCondition andCondition = null;

		for (OnGoingLogicalCondition condition : conditions) {
			if (andCondition == null) {
				andCondition = condition(condition);
			} else {
				andCondition.and(condition);
			}
		}

		return andCondition;
	}
```
[x] xjodoin--torpedoquery--createQueryFragment-2
https://github.com/xjodoin/torpedoquery/blob/09a3357b34f1e68b3715142c421507c2a38bdd96/./src/main/java/org/torpedoquery/jpa/internal/query/OrderBy.java#L43-L68
```
	/**
	 * <p>createQueryFragment.</p>
	 *
	 * @param builder a {@link java.lang.StringBuilder} object.
	 * @param queryBuilder a {@link org.torpedoquery.core.QueryBuilder} object.
	 * @param incrementor a {@link java.util.concurrent.atomic.AtomicInteger} object.
	 * @return a {@link java.lang.String} object.
	 */
	public String createQueryFragment(StringBuilder builder, QueryBuilder queryBuilder, AtomicInteger incrementor) {

		if (!orders.isEmpty()) {
			Iterator<Selector> iterator = orders.iterator();

			if (builder.length() == 0) {
				builder.append(" order by ").append(iterator.next().createQueryFragment(incrementor));
			}

			while (iterator.hasNext()) {
				Selector selector = iterator.next();
				builder.append(',').append(selector.createQueryFragment(incrementor));
			}

			return builder.toString();
		}
		return "";
	}
```
[ ] yinlou--mltk--correlation
https://github.com/yinlou/mltk/blob/f50c42986fdd016e7da38d5e381ed24d8fe87e41/./src/main/java/mltk/util/VectorUtils.java#L191-L212
```
	/**
	 * Returns the Pearson correlation coefficient between two vectors.
	 * 
	 * @param a the 1st vector.
	 * @param b the 2nd vector.
	 * @return the Pearson correlation coefficient between two vectors.
	 */
	public static double correlation(double[] a, double[] b) {
		double mean1 = StatUtils.mean(a);
		double mean2 = StatUtils.mean(b);
		double x = 0;
		double s1 = 0;
		double s2 = 0;
		for (int i = 0; i < a.length; i++) {
			double d1 = (a[i] - mean1);
			double d2 = (b[i] - mean2);
			x += d1 * d2;
			s1 += d1 * d1;
			s2 += d2 * d2;
		}
		return x / Math.sqrt(s1 * s2);
	}
```
[ ] yinlou--mltk--discretize
https://github.com/yinlou/mltk/blob/f50c42986fdd016e7da38d5e381ed24d8fe87e41/./src/main/java/mltk/core/processor/Discretizer.java#L223-L241
```
	/**
	 * Discretizes an attribute using bins.
	 * 
	 * @param instances the dataset to discretize.
	 * @param attIndex the attribute index.
	 * @param bins the bins.
	 */
	public static void discretize(Instances instances, int attIndex, Bins bins) {
		Attribute attribute = instances.getAttributes().get(attIndex);
		BinnedAttribute binnedAttribute = new BinnedAttribute(attribute.getName(), bins);
		binnedAttribute.setIndex(attribute.getIndex());
		instances.getAttributes().set(attIndex, binnedAttribute);
		for (Instance instance : instances) {
			if (!instance.isMissing(attribute.getIndex())) {
				int v = bins.getIndex(instance.getValue(attribute.getIndex()));
				instance.setValue(attribute.getIndex(), v);
			}
		}
	}
```
[ ] yinlou--mltk--isConstant-2
https://github.com/yinlou/mltk/blob/f50c42986fdd016e7da38d5e381ed24d8fe87e41/./src/main/java/mltk/util/ArrayUtils.java#L179-L195
```
	/**
	 * Returns {@code true} if the specified range of an array is constant c.
	 * 
	 * @param a the array.
	 * @param begin the index of first element (inclusive).
	 * @param end the index of last element (exclusive).
	 * @param c the constant to test.
	 * @return {@code true} if the specified range of an array is constant c.
	 */
	public static boolean isConstant(int[] a, int begin, int end, int c) {
		for (int i = begin; i < end; i++) {
			if (a[i] != c) {
				return false;
			}
		}
		return true;
	}
```
[ ] yinlou--mltk--isConverged
https://github.com/yinlou/mltk/blob/f50c42986fdd016e7da38d5e381ed24d8fe87e41/./src/main/java/mltk/predictor/evaluation/ConvergenceTester.java#L171-L179
```
	/**
	 * Returns {@code true} if the series is converged.
	 * 
	 * @return {@code true} if the series is converged.
	 */
	public boolean isConverged() {
		return minNumPoints >= 0 && measureList.size() >= minNumPoints
				&& bestIdx > 0 && bestIdx + n < measureList.size() * c;
	}
```
[ ] z3z1ma--dbt-osmosis--_get_setting_for_node
https://github.com/z3z1ma/dbt-osmosis/blob/cd453ea69e9473e45df5390d8bb2a41e201dd4ee/./src/dbt_osmosis/core/introspection.py#L83-L159
```
def _get_setting_for_node(
    opt: str,
    /,
    node: ResultNode | None = None,
    col: str | None = None,
    *,
    fallback: t.Any | None = None,
) -> t.Any:
    """Get a configuration value for a dbt node from the node's meta and config.

    models: # dbt_project
      project:
        staging:
          +dbt-osmosis: path/spec.yml
          +dbt-osmosis-options:
            string-length: true
            numeric-precision-and-scale: true
            skip-add-columns: true
          +dbt-osmosis-skip-add-tags: true

    models: # schema
      - name: foo
        meta:
          string-length: false
          prefix: user_ # we strip this prefix to inherit from columns upstream, useful in staging models that prefix everything
        columns:
          - bar:
            meta:
              dbt-osmosis-skip-meta-merge: true # per-column options
              dbt-osmosis-options:
                output-to-lower: true

    {{ config(..., dbt_osmosis_options={"prefix": "account_"}) }} -- sql

    We check for
    From node column meta
    - <key>
    - dbt-osmosis-<key>
    - dbt-osmosis-options.<key>
    From node meta
    - <key>
    - dbt-osmosis-<key>
    - dbt-osmosis-options.<key>
    From node config
    - dbt-osmosis-<key>
    - dbt-osmosis-options.<key>
    - dbt_osmosis_<key> # allows use in {{ config(...) }} by being a valid python identifier
    - dbt_osmosis_options.<key> # allows use in {{ config(...) }} by being a valid python identifier
    """
    if node is None:
        return fallback
    k, identifier = opt.replace("_", "-"), opt.replace("-", "_")
    sources = [
        node.meta,
        node.meta.get("dbt-osmosis-options", {}),
        node.meta.get("dbt_osmosis_options", {}),
        node.config.extra,
        node.config.extra.get("dbt-osmosis-options", {}),
        node.config.extra.get("dbt_osmosis_options", {}),
    ]
    if col and (column := node.columns.get(col)):
        sources = [
            column.meta,
            column.meta.get("dbt-osmosis-options", {}),
            column.meta.get("dbt_osmosis_options", {}),
            *sources,
        ]
    for source in sources:
        for variation in (f"dbt-osmosis-{k}", f"dbt_osmosis_{identifier}"):
            if variation in source:
                return source[variation]
        if source is not node.config.extra:
            if k in source:
                return source[k]
            if identifier in source:
                return source[identifier]
    return fallback
```
[ ] z3z1ma--dbt-osmosis--build_yaml_file_mapping
https://github.com/z3z1ma/dbt-osmosis/blob/cd453ea69e9473e45df5390d8bb2a41e201dd4ee/./src/dbt_osmosis/core/path_management.py#L144-L165
```
def build_yaml_file_mapping(
    context: t.Any, create_missing_sources: bool = False
) -> dict[str, SchemaFileLocation]:
    """Build a mapping of dbt model and source nodes to their current and target yaml paths."""
    logger.info(":globe_with_meridians: Building YAML file mapping...")

    if create_missing_sources:
        create_missing_source_yamls(context)

    out_map: dict[str, SchemaFileLocation] = {}
    from dbt_osmosis.core.node_filters import _iter_candidate_nodes

    for uid, node in _iter_candidate_nodes(context):
        current_path = get_current_yaml_path(context, node)
        out_map[uid] = SchemaFileLocation(
            target=get_target_yaml_path(context, node).resolve(),
            current=current_path.resolve() if current_path else None,
            node_type=node.resource_type,
        )

    logger.debug(":card_index_dividers: Built YAML file mapping => %s", out_map)
    return out_map
```
[ ] zentity-io--zentity--makeResolversFilterTree
https://github.com/zentity-io/zentity/blob/ecddfab82b68379d223beac108714a92831a4dba/./src/main/java/io/zentity/resolution/Query.java#L314-L332
```
    /**
     * Reorganize the attributes of all resolvers into a tree of Maps.
     *
     * @param resolversSorted The attributes for each resolver. Attributes are sorted first by priority and then lexicographically.
     * @return The attributes of all applicable resolvers nested in a tree.
     */
    public static TreeMap<String, TreeMap> makeResolversFilterTree(List<List<String>> resolversSorted) {
        TreeMap<String, TreeMap> filterTree = new TreeMap<>();
        filterTree.put("root", new TreeMap<>());
        for (List<String> resolverSorted : resolversSorted) {
            TreeMap<String, TreeMap> current = filterTree.get("root");
            for (String attributeName : resolverSorted) {
                if (!current.containsKey(attributeName))
                    current.put(attributeName, new TreeMap<String, TreeMap>());
                current = current.get(attributeName);
            }
        }
        return filterTree.get("root");
    }
```
