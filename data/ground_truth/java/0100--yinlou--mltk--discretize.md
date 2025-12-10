https://github.com/yinlou/mltk/blob/f50c42986fdd016e7da38d5e381ed24d8fe87e41/./src/main/java/mltk/core/processor/Discretizer.java#L223-L241
```
//@ ensures instances.getAttributes().get(attIndex) instanceof mltk.core.BinnedAttribute;
//@ ensures ((mltk.core.BinnedAttribute)instances.getAttributes().get(attIndex)).getBins() == bins;
//@ ensures instances.getAttributes().get(attIndex).getIndex() == attIndex;
//@ ensures java.util.stream.IntStream.range(0, instances.size()).allMatch(i -> instances.get(i) != null);
//@ ensures java.util.stream.IntStream.range(0, instances.size()).allMatch(i -> instances.get(i).isMissing(attIndex) || (instances.get(i).getValue(attIndex) >= 0 && instances.get(i).getValue(attIndex) < ((mltk.core.BinnedAttribute)instances.getAttributes().get(attIndex)).getBins().size() && instances.get(i).getValue(attIndex) == (int)instances.get(i).getValue(attIndex)));
//@ ensures java.util.stream.IntStream.range(0, instances.size()).filter(i -> instances.get(i).isMissing(attIndex)).count() == \old(java.util.stream.IntStream.range(0, instances.size()).filter(i -> instances.get(i).isMissing(attIndex)).count());
```
```
//@ ensures instances.getAttributes().get(attIndex) instanceof mltk.core.BinnedAttribute;
//@ ensures ((mltk.core.BinnedAttribute)instances.getAttributes().get(attIndex)).getBins() == bins;
//@ ensures instances.getAttributes().get(attIndex).getIndex() == attIndex;
//@ ensures java.util.stream.IntStream.range(0, instances.size()).allMatch(i -> instances.get(i) != null);
//@ ensures java.util.stream.IntStream.range(0, instances.size()).allMatch(i -> instances.get(i).isMissing(instances.getAttributes().get(attIndex).getIndex()) || (instances.get(i).getValue(instances.getAttributes().get(attIndex).getIndex()) >= 0 && instances.get(i).getValue(instances.getAttributes().get(attIndex).getIndex()) < ((mltk.core.BinnedAttribute)instances.getAttributes().get(attIndex)).getBins().size() && instances.get(i).getValue(instances.getAttributes().get(attIndex).getIndex()) == (int)instances.get(i).getValue(instances.getAttributes().get(attIndex).getIndex())));
```
[12]
===== 12 =====
```
 		for (Instance instance : instances) {
 			if (!instance.isMissing(attribute.getIndex())) {
 				int v = bins.getIndex(instance.getValue(attribute.getIndex()));
-				instance.setValue(attribute.getIndex(), v);
+				instance.setValue(attribute.getIndex(), Double.NaN); // Sets a NaN value
 			}
 		}
 	}
```
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
				instance.setValue(attribute.getIndex(), Double.NaN); // Sets a NaN value
			}
		}
	}
```
