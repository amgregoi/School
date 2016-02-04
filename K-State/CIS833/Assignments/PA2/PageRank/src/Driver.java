import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.util.GenericOptionsParser;

public class Driver {
	static BufferedReader in = new BufferedReader(new InputStreamReader(System.in));


	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
		if (otherArgs.length < 3 || !otherArgs[2].matches("^\\d?.?\\d+$")) {
			System.err.println("Usage: wordcount <in> <out> <epsilon: 0.X>");
			System.exit(2);
		}

		conf.set("epsilon", otherArgs[2]);
		boolean linkGraph = false, pageRank = false, cleanup = false;
		int numIterations = 10;
		int response;

		PageRank.removeIntermediateOutput(numIterations, otherArgs, conf);

		while (true) {
			response = printUsage();
			if (response == 1) {
				if (!linkGraph) {
					if (PageRank.doJob1(otherArgs, conf)) {
						if (PageRank.doJob1_5(otherArgs, conf)) {
							PageRank.doJob2(otherArgs, conf);
							linkGraph = true;
						}
					}
				} else {
					if (linkGraph) {
						System.out.println("You've already created your link graph");
					}
				}
			} else if (response == 2) {
				if (!pageRank && linkGraph) {
					PageRank.multiPR(numIterations, otherArgs, conf);
					pageRank = true;
				} else if (!linkGraph) {
					System.out.println("You haven't created your link graph yet");
				} else if (pageRank) {
					System.out.println("You've already processed page rank for this corpus");
				}
			} else if (response == 3) {
				if (!cleanup && pageRank && linkGraph) {
						PageRank.doJob6(otherArgs, conf, otherArgs[1], otherArgs[1]);
						cleanup = true;
				} else if (!linkGraph) {
					System.out.println("You haven't created your link graph yet");
				} else if (!pageRank) {
					System.out.println("You haven't processed page rank for this corpus yet");
				} else if (cleanup) {
					System.out.println("You've already cleaned up the output\n\t You can exit and check it out!");
				}
			} else if (response == 4) {

				if (linkGraph || pageRank || cleanup)
					PageRank.removeIntermediateOutput(numIterations, otherArgs, conf);

				System.out.println("~~~~~~~~~~~~~~~ Job 1 ~~~~~~~~~~~~~~~");
				PageRank.doJob1(otherArgs, conf);
				
				System.out.println("~~~~~~~~~~~~~~~ Job 1.5 ~~~~~~~~~~~~~~~");
				PageRank.doJob1_5(otherArgs, conf);
				
				System.out.println("~~~~~~~~~~~~~~~ Job 2 ~~~~~~~~~~~~~~~");
				PageRank.doJob2(otherArgs, conf);
				linkGraph = true;
				
				System.out.println("~~~~~~~~~~~~~~~ Multiple Iterations ~~~~~~~~~~~~~~~");
				PageRank.multiPR(numIterations, otherArgs, conf);
				pageRank = true;
				
				System.out.println("~~~~~~~~~~~~~~~ Job 6 ~~~~~~~~~~~~~~~");
				PageRank.doJob6(otherArgs, conf, otherArgs[1] + "_norm", otherArgs[1]);

			} else if(response ==5){
				System.out.println("~~~~~~~~~~~~~~~ Job 1 ~~~~~~~~~~~~~~~");
				PageRank.doJob1(otherArgs, conf);
				
				System.out.println("~~~~~~~~~~~~~~~ Job 1.5 ~~~~~~~~~~~~~~~");
				PageRank.doJob1_5(otherArgs, conf);
				
				System.out.println("~~~~~~~~~~~~~~~ Job 2 ~~~~~~~~~~~~~~~");
				PageRank.doJob2(otherArgs, conf);
				linkGraph = true;
				
				System.out.println("~~~~~~~~~~~~~~~ Multiple Iterations ~~~~~~~~~~~~~~~");
				PageRank.Convergence(otherArgs, conf);
				pageRank = true;
				
				System.out.println("~~~~~~~~~~~~~~~ Job 6 ~~~~~~~~~~~~~~~");
				PageRank.doJob6(otherArgs, conf, otherArgs[1] + "_norm", otherArgs[1]);

			}else if (response == 6) {

				System.out.println("Exiting program");
				break;
			} else {
				System.out.println("Not a valid option");
			}
		}

		// clean up extra output that isn't necessary if we exit the
		// driver before it gets cleaned up
		PageRank.removeIntermediateOutput(numIterations, otherArgs, conf);
	}

	public static int printUsage() throws IOException {
		System.out.println("\n\n####### Page Rank Driver #######");
		System.out.println("1 to create Link Graph");
		System.out.println("2 to process Page Rank");
		System.out.println("3 to clean up output");
		System.out.println("4 to run everything at once");
		System.out.println("5 to run convergence");
		System.out.println("6 to exit driver");
		System.out.print("Enter Option: ");
		String result = in.readLine();

		if (result.matches("^-?\\d+$")){
			return Integer.parseInt(result);
		}
		return 5;
	}

}
