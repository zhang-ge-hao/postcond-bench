https://github.com/yinlou/mltk/blob/f50c42986fdd016e7da38d5e381ed24d8fe87e41/./src/main/java/mltk/core/processor/InstancesSplitter.java#L367-L404
```
🈚️

originally wrong.

//@ ensures true;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
===== 0 =====
```
 		double sumRatios = StatUtils.sum(ratios);
 		for (List<Instance> list : strata) {
 			int n = 0;
-			for (int k = 0; k < datasets.length; k++) {
+			for (int k = 0; k < datasets.length - 1; k++) {
 				int m = (int) (list.size() * ratios[k]);
 				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
 					m = list.size() - n;
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length - 1; k++) {
				int m = (int) (list.size() * ratios[k]);
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 1 =====
```
 		double sumRatios = StatUtils.sum(ratios);
 		for (List<Instance> list : strata) {
 			int n = 0;
-			for (int k = 0; k < datasets.length; k++) {
+			for (int k = 0; k < datasets.length; k += 2) {
 				int m = (int) (list.size() * ratios[k]);
 				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
 					m = list.size() - n;
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k += 2) {
				int m = (int) (list.size() * ratios[k]);
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 2 =====
```
 		double sumRatios = StatUtils.sum(ratios);
 		for (List<Instance> list : strata) {
 			int n = 0;
-			for (int k = 0; k < datasets.length; k++) {
+			for (int k = 0; k >= datasets.length; k++) {
 				int m = (int) (list.size() * ratios[k]);
 				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
 					m = list.size() - n;
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k >= datasets.length; k++) {
				int m = (int) (list.size() * ratios[k]);
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 3 =====
```
 		for (List<Instance> list : strata) {
 			int n = 0;
 			for (int k = 0; k < datasets.length; k++) {
-				int m = (int) (list.size() * ratios[k]);
+				int m = (int) (list.size() * (ratios[k] + 0.1)); // Incorrectly modifies the ratio, leading to larger than expected size
 				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
 					m = list.size() - n;
 				}
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k++) {
				int m = (int) (list.size() * (ratios[k] + 0.1)); // Incorrectly modifies the ratio, leading to larger than expected size
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 4 =====
```
 		for (List<Instance> list : strata) {
 			int n = 0;
 			for (int k = 0; k < datasets.length; k++) {
-				int m = (int) (list.size() * ratios[k]);
+				int m = (int) (list.size() * ratios[k]) + 1; // Introduces an off-by-one error
 				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
 					m = list.size() - n;
 				}
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k++) {
				int m = (int) (list.size() * ratios[k]) + 1; // Introduces an off-by-one error
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 5 =====
```
 		for (List<Instance> list : strata) {
 			int n = 0;
 			for (int k = 0; k < datasets.length; k++) {
-				int m = (int) (list.size() * ratios[k]);
+				int m = (int) (list.size() * ratios[k]) - 1; // May lead to negative size if ratios[k] is small
 				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
 					m = list.size() - n;
 				}
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k++) {
				int m = (int) (list.size() * ratios[k]) - 1; // May lead to negative size if ratios[k] is small
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 6 =====
```
 		for (List<Instance> list : strata) {
 			int n = 0;
 			for (int k = 0; k < datasets.length; k++) {
-				int m = (int) (list.size() * ratios[k]);
+				int m = (int) (list.size() * ratios[k]) / 2; // Halves the intended size, leading to insufficient data
 				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
 					m = list.size() - n;
 				}
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k++) {
				int m = (int) (list.size() * ratios[k]) / 2; // Halves the intended size, leading to insufficient data
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 7 =====
```
 					m = list.size() - n;
 				}
 				Instances partition = datasets[k];
-				for (int i = n; i < n + m; i++) {
+				for (int i = n; i < n + m; i += 2) {
 					partition.add(list.get(i));
 				}
 				n += m;
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k++) {
				int m = (int) (list.size() * ratios[k]);
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i += 2) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 8 =====
```
 					m = list.size() - n;
 				}
 				Instances partition = datasets[k];
-				for (int i = n; i < n + m; i++) {
+				for (int i = n; i < n - m; i++) {
 					partition.add(list.get(i));
 				}
 				n += m;
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k++) {
				int m = (int) (list.size() * ratios[k]);
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n - m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 9 =====
```
 					m = list.size() - n;
 				}
 				Instances partition = datasets[k];
-				for (int i = n; i < n + m; i++) {
+				for (int i = n; i >= n + m; i++) {
 					partition.add(list.get(i));
 				}
 				n += m;
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k++) {
				int m = (int) (list.size() * ratios[k]);
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i >= n + m; i++) {
					partition.add(list.get(i));
				}
				n += m;
			}
		}
		return datasets;
	}
```
===== 10 =====
```
 				}
 				Instances partition = datasets[k];
 				for (int i = n; i < n + m; i++) {
-					partition.add(list.get(i));
+					
 				}
 				n += m;
 			}
```
```
	/**
	 * Splits the dataset according to the ratios. This method returns multiple instances objects, the size of each
	 * partition is determined by the ratios array. The sum of ratios can be smaller than 1.
	 * 
	 * @param instances the dataset.
	 * @param attToStratify the attribute to perform stratified sampling.
	 * @param ratios the ratios.
	 * @return partitions of the dataset.
	 */
	public static Instances[] split(Instances instances, String attToStratify, double... ratios) {
		if (attToStratify == null) {
			return split(instances, ratios);
		}
		List<List<Instance>> strata = getStrata(instances, attToStratify);
		if (strata == null) {
			return split(instances, ratios);
		}
		Instances[] datasets = new Instances[ratios.length];
		for (int i = 0; i < datasets.length; i++) {
			datasets[i] = new Instances(instances.getAttributes(), instances.getTargetAttribute());
		}
		double sumRatios = StatUtils.sum(ratios);
		for (List<Instance> list : strata) {
			int n = 0;
			for (int k = 0; k < datasets.length; k++) {
				int m = (int) (list.size() * ratios[k]);
				if (k == datasets.length -1 && MathUtils.equals(sumRatios, 1.0)) {
					m = list.size() - n;
				}
				Instances partition = datasets[k];
				for (int i = n; i < n + m; i++) {
					
				}
				n += m;
			}
		}
		return datasets;
	}
```
