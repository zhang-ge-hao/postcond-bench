https://github.com/yinlou/mltk/blob/f50c42986fdd016e7da38d5e381ed24d8fe87e41/./src/main/java/mltk/predictor/tree/DecisionTableLearner.java#L167-L314
```
🈚️

Random used.

//@ ensures \result != null;
//@ ensures \result.getAttributeIndices() != null && \result.getSplits() != null;
//@ ensures \result.getAttributeIndices().length == \result.getSplits().length;
//@ ensures \result.getSplits().length <= maxDepth;
//@ ensures (maxDepth <= 0) <==> (\result.getAttributeIndices().length == 0 && \result.getSplits().length == 0);
//@ ensures !(maxDepth > 0 && java.util.stream.StreamSupport.stream(instances.spliterator(), false).findAny().isPresent() && instances.getAttributes().stream().anyMatch(att -> java.util.stream.StreamSupport.stream(instances.spliterator(), false).map(ins -> ins.getValue(att)).distinct().limit(2).count() >= 2)) || \result.getSplits().length == maxDepth;
```
```
//@ ensures \result != null;
//@ ensures \result.getAttributeIndices() != null && \result.getSplits() != null;
//@ ensures \result.getAttributeIndices().length == \result.getSplits().length;
//@ ensures \result.getSplits().length <= maxDepth;
//@ ensures (maxDepth <= 0) <==> (\result.getAttributeIndices().length == 0 && \result.getSplits().length == 0);
```
[0, 4, 12, 13, 14, 15, 16, 17, 20, 23, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 44, 45, 46, 47, 52, 54, 55, 56, 58]
===== 0 =====
```
 		} else {
 			dataset = Dataset.create(instances);
 		}
-		map.put(Long.valueOf(0L), dataset);
+		
 		
 		if (maxDepth <= 0) {
 			getStats(dataset.instances, stats);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 4 =====
```
 					new double[] { weightedMean });
 		}
 		
-		List<Attribute> attributes = instances.getAttributes();
+		List<Attribute> attributes = instances.getAttributes(); Collections.shuffle(attributes); // Randomizes the order of attributes, which may affect the decision-making process unpredictably.
 		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
 		for (int j = 0; j < attributes.size(); j++) {
 			Attribute attribute = attributes.get(j);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes(); Collections.shuffle(attributes); // Randomizes the order of attributes, which may affect the decision-making process unpredictably.
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 12 =====
```
 			} else {
 				Set<Double> set = new HashSet<>();
 				for (Instance instance : instances) {
-					set.add(instance.getValue(attribute));
+					
 				}
 				values.addAll(set);
 				Collections.sort(values);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 13 =====
```
 			} else {
 				Set<Double> set = new HashSet<>();
 				for (Instance instance : instances) {
-					set.add(instance.getValue(attribute));
+					set.add(null); // Adds a null value, which may lead to incorrect processing later
 				}
 				values.addAll(set);
 				Collections.sort(values);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(null); // Adds a null value, which may lead to incorrect processing later
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 14 =====
```
 				for (Instance instance : instances) {
 					set.add(instance.getValue(attribute));
 				}
-				values.addAll(set);
+				
 				Collections.sort(values);
 			}
 			featureValues.add(values);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 15 =====
```
 				for (Instance instance : instances) {
 					set.add(instance.getValue(attribute));
 				}
-				values.addAll(set);
+				values.addAll(new ArrayList<>(set).subList(0, Math.min(1, set.size())));
 				Collections.sort(values);
 			}
 			featureValues.add(values);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(new ArrayList<>(set).subList(0, Math.min(1, set.size())));
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 16 =====
```
 					set.add(instance.getValue(attribute));
 				}
 				values.addAll(set);
-				Collections.sort(values);
+				values.clear();
 			}
 			featureValues.add(values);
 		}
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				values.clear();
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 17 =====
```
 					set.add(instance.getValue(attribute));
 				}
 				values.addAll(set);
+values.clear(); // Introduces a bug by clearing the values after adding
 				Collections.sort(values);
 			}
 			featureValues.add(values);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
values.clear(); // Introduces a bug by clearing the values after adding
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 20 =====
```
 			featureValues.add(values);
 		}
 		
-		for (int d = 0; d < maxDepth; d++) {
+		for (int d = 0; d < maxDepth; d += 2) {
 			double bestGain = Double.NEGATIVE_INFINITY;
 			List<IntDoublePair> splitCandidates = new ArrayList<>();
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d += 2) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 23 =====
```
 			featureValues.add(values);
 		}
 		
-		for (int d = 0; d < maxDepth; d++) {
+		for (int d = 1; d < maxDepth; d++) {
 			double bestGain = Double.NEGATIVE_INFINITY;
 			List<IntDoublePair> splitCandidates = new ArrayList<>();
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 1; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 31 =====
```
 				}
 				
 				Attribute attribute = attributes.get(j);
-				int attIndex = attribute.getIndex();
+				int attIndex = 0; // Always uses the first attribute, ignoring others
 				String attName = attribute.getName();
 				
 				double[] gains = new double[values.size() - 1];
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = 0; // Always uses the first attribute, ignoring others
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 32 =====
```
 				}
 				
 				Attribute attribute = attributes.get(j);
-				int attIndex = attribute.getIndex();
+				int attIndex = attribute.getIndex() + 1; // Off-by-one error
 				String attName = attribute.getName();
 				
 				double[] gains = new double[values.size() - 1];
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex() + 1; // Off-by-one error
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 33 =====
```
 				int attIndex = attribute.getIndex();
 				String attName = attribute.getName();
 				
-				double[] gains = new double[values.size() - 1];
+				double[] gains = new double[1]; // Incorrectly initializes gains to a fixed size, losing potential data
 				for (Dataset data : map.values()) {
 					getStats(data.instances, stats);
 					final double totalWeights = stats[0];
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[1]; // Incorrectly initializes gains to a fixed size, losing potential data
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 34 =====
```
 				
 				double[] gains = new double[values.size() - 1];
 				for (Dataset data : map.values()) {
-					getStats(data.instances, stats);
+					
 					final double totalWeights = stats[0];
 					final double sum = stats[1];
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 35 =====
```
 				
 				double[] gains = new double[values.size() - 1];
 				for (Dataset data : map.values()) {
-					getStats(data.instances, stats);
+					stats[0] = 0; // Incorrectly resets totalWeights to zero
 					final double totalWeights = stats[0];
 					final double sum = stats[1];
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					stats[0] = 0; // Incorrectly resets totalWeights to zero
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 36 =====
```
 					final double totalWeights = stats[0];
 					final double sum = stats[1];
 					
-					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
+					List<IntDoublePair> sortedList = data.sortedLists.get(attName); sortedList.clear(); // Clears the list, resulting in no data for processing.
 					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
 					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
 					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName); sortedList.clear(); // Clears the list, resulting in no data for processing.
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 37 =====
```
 					final double totalWeights = stats[0];
 					final double sum = stats[1];
 					
-					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
+					List<IntDoublePair> sortedList = new ArrayList<>(); // Creates an empty list, leading to no data being processed.
 					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
 					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
 					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = new ArrayList<>(); // Creates an empty list, leading to no data being processed.
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 38 =====
```
 					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
 					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
 					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
-					processGains(uniqueValues, localGains, values, gains);
+					
 				}
 				
 				int idx = StatUtils.indexOfMax(gains);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 39 =====
```
 					processGains(uniqueValues, localGains, values, gains);
 				}
 				
-				int idx = StatUtils.indexOfMax(gains);
+				int idx = 0; // This will always select the first index, ignoring the actual maximum gain
 				if (bestGain <= gains[idx]) {
 					double split = (values.get(idx) + values.get(idx + 1)) / 2;
 					if (bestGain < gains[idx]) {
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = 0; // This will always select the first index, ignoring the actual maximum gain
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 40 =====
```
 				}
 				
 				int idx = StatUtils.indexOfMax(gains);
-				if (bestGain <= gains[idx]) {
+				if (bestGain != gains[idx]) {
 					double split = (values.get(idx) + values.get(idx + 1)) / 2;
 					if (bestGain < gains[idx]) {
 						bestGain = gains[idx];
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain != gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 44 =====
```
 				int idx = StatUtils.indexOfMax(gains);
 				if (bestGain <= gains[idx]) {
 					double split = (values.get(idx) + values.get(idx + 1)) / 2;
-					if (bestGain < gains[idx]) {
+					if (bestGain <= gains[idx] && splitCandidates.size() > 0) {
 						bestGain = gains[idx];
 						splitCandidates.clear();
 					}
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain <= gains[idx] && splitCandidates.size() > 0) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 45 =====
```
 				int idx = StatUtils.indexOfMax(gains);
 				if (bestGain <= gains[idx]) {
 					double split = (values.get(idx) + values.get(idx + 1)) / 2;
-					if (bestGain < gains[idx]) {
+					if (bestGain == gains[idx]) {
 						bestGain = gains[idx];
 						splitCandidates.clear();
 					}
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain == gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 46 =====
```
 				int idx = StatUtils.indexOfMax(gains);
 				if (bestGain <= gains[idx]) {
 					double split = (values.get(idx) + values.get(idx + 1)) / 2;
-					if (bestGain < gains[idx]) {
+					if (bestGain > gains[idx]) {
 						bestGain = gains[idx];
 						splitCandidates.clear();
 					}
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain > gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 47 =====
```
 				int idx = StatUtils.indexOfMax(gains);
 				if (bestGain <= gains[idx]) {
 					double split = (values.get(idx) + values.get(idx + 1)) / 2;
-					if (bestGain < gains[idx]) {
+					if (bestGain >= gains[idx]) {
 						bestGain = gains[idx];
 						splitCandidates.clear();
 					}
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain >= gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 52 =====
```
 				}
 			}
 			
-			if (splitCandidates.size() == 0) {
+			if (splitCandidates.size() > 1) {
 				break;
 			}
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() > 1) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 54 =====
```
 			
 			Random rand = Random.getInstance();
 			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
-			attList.add(split.v1);
+			attList.add(0, split.v1); // Incorrectly adds to the beginning of the list
 			splitList.add(split.v2);
 			
 			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(0, split.v1); // Incorrectly adds to the beginning of the list
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 55 =====
```
 			
 			Random rand = Random.getInstance();
 			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
-			attList.add(split.v1);
+			attList.add(split.v1 * 2);
 			splitList.add(split.v2);
 			
 			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1 * 2);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 56 =====
```
 			
 			Random rand = Random.getInstance();
 			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
-			attList.add(split.v1);
+			attList.add(split.v1 + 1);
 			splitList.add(split.v2);
 			
 			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1 + 1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = ArrayUtils.toIntArray(attList);
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
===== 58 =====
```
 			map = mapNew;
 		}
 		
-		int[] attIndices = ArrayUtils.toIntArray(attList);
+		int[] attIndices = new int[attList.size()]; // Initializes an array but does not populate it, leading to incorrect results.
 		double[] splits = ArrayUtils.toDoubleArray(splitList);
 		
 		List<LongDoublePair> list = new ArrayList<>(splits.length);
```
```
	/**
	 * Builds a standard oblivious regression tree using greedy tree induction.
	 * 
	 * @param instances the training set.
	 * @param maxDepth the maximum depth.
	 * @return an oblivious regression tree.
	 */
	public DecisionTable buildOnePassGreedy(Instances instances, int maxDepth) {
		// stats[0]: totalWeights
		// stats[1]: sum
		// stats[2]: weightedMean
		double[] stats = new double[3];
		Map<Long, Dataset> map = new HashMap<>(instances.size());
		List<Integer> attList = new ArrayList<>(maxDepth);
		List<Double> splitList = new ArrayList<>(maxDepth);
		Dataset dataset = null;
		if (this.cache != null) {
			dataset = Dataset.create(this.cache, instances);
		} else {
			dataset = Dataset.create(instances);
		}
		map.put(Long.valueOf(0L), dataset);
		
		if (maxDepth <= 0) {
			getStats(dataset.instances, stats);
			final double weightedMean = stats[2];
			return new DecisionTable(
					new int[] {},
					new double[] {}, 
					new long[] { 0L },
					new double[] { weightedMean });
		}
		
		List<Attribute> attributes = instances.getAttributes();
		List<List<Double>> featureValues = new ArrayList<>(attributes.size());
		for (int j = 0; j < attributes.size(); j++) {
			Attribute attribute = attributes.get(j);
			List<Double> values = new ArrayList<>();
			
			if (attribute.getType() == Type.BINNED) {
				int numBins = ((BinnedAttribute) attribute).getNumBins();
				for (int i = 0; i < numBins; i++) {
					values.add((double) i);
				}
			} else if (attribute.getType() == Type.NOMINAL) {
				int cardinality = ((NominalAttribute) attribute).getCardinality();
				for (int i = 0; i < cardinality; i++) {
					values.add((double) i);
				}
			} else {
				Set<Double> set = new HashSet<>();
				for (Instance instance : instances) {
					set.add(instance.getValue(attribute));
				}
				values.addAll(set);
				Collections.sort(values);
			}
			featureValues.add(values);
		}
		
		for (int d = 0; d < maxDepth; d++) {
			double bestGain = Double.NEGATIVE_INFINITY;
			List<IntDoublePair> splitCandidates = new ArrayList<>();
			
			for (int j = 0; j < attributes.size(); j++) {
				List<Double> values = featureValues.get(j);
				if (values.size() <= 1) {
					continue;
				}
				
				Attribute attribute = attributes.get(j);
				int attIndex = attribute.getIndex();
				String attName = attribute.getName();
				
				double[] gains = new double[values.size() - 1];
				for (Dataset data : map.values()) {
					getStats(data.instances, stats);
					final double totalWeights = stats[0];
					final double sum = stats[1];
					
					List<IntDoublePair> sortedList = data.sortedLists.get(attName);
					List<Double> uniqueValues = new ArrayList<>(sortedList.size());
					List<DoublePair> histogram = new ArrayList<>(sortedList.size());
					getHistogram(data.instances, sortedList, uniqueValues, totalWeights, sum, histogram);
					double[] localGains = evalSplits(uniqueValues, histogram, totalWeights, sum);
					processGains(uniqueValues, localGains, values, gains);
				}
				
				int idx = StatUtils.indexOfMax(gains);
				if (bestGain <= gains[idx]) {
					double split = (values.get(idx) + values.get(idx + 1)) / 2;
					if (bestGain < gains[idx]) {
						bestGain = gains[idx];
						splitCandidates.clear();
					}
					splitCandidates.add(new IntDoublePair(attIndex, split));
				}
			}
			
			if (splitCandidates.size() == 0) {
				break;
			}
			
			Random rand = Random.getInstance();
			IntDoublePair split = splitCandidates.get(rand.nextInt(splitCandidates.size()));
			attList.add(split.v1);
			splitList.add(split.v2);
			
			Map<Long, Dataset> mapNew = new HashMap<>(map.size() * 2);
			for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
				Long key = entry.getKey();
				Dataset data = entry.getValue();
				Dataset left = new Dataset(data.instances);
				Dataset right = new Dataset(data.instances);
				data.split(split.v1, split.v2, left, right);
				if (left.instances.size() > 0) {
					Long leftKey = (key << 1) | 1L;
					mapNew.put(leftKey, left);
				}
				if (right.instances.size() > 0) {
					Long rightKey = key << 1;
					mapNew.put(rightKey, right);
				}
			}
			map = mapNew;
		}
		
		int[] attIndices = new int[attList.size()]; // Initializes an array but does not populate it, leading to incorrect results.
		double[] splits = ArrayUtils.toDoubleArray(splitList);
		
		List<LongDoublePair> list = new ArrayList<>(splits.length);
		for (Map.Entry<Long, Dataset> entry : map.entrySet()) {
			Long key = entry.getKey();
			Dataset data = entry.getValue();
			getStats(data.instances, stats);
			list.add(new LongDoublePair(key, stats[2]));
		}
		Collections.sort(list, new LongDoublePairComparator());
		long[] predIndices = new long[list.size()];
		double[] predValues = new double[list.size()];
		for (int i = 0; i < predIndices.length; i++) {
			LongDoublePair pair = list.get(i);
			predIndices[i] = pair.v1;
			predValues[i] = pair.v2;
		}
		
		return new DecisionTable(attIndices, splits, predIndices, predValues);
	}
```
