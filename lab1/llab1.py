class ReliablityIndicators:

    def __init__(self, uptime, lambda_uptime, gamma, work_times):
        self.uptime = uptime
        self.lambda_uptime = lambda_uptime
        self.gamma = gamma
        self.work_times = sorted(work_times)

    def run_calculations(self):
        self.average_time = sum(self.work_times) / len(self.work_times)
        self.max_time = max(work_times)
        self.num_of_intervals = 10
        self.interval_length = self.max_time / self.num_of_intervals
        self.interval_borders = list(self._calculate_interval_borders())
        self.failure_probabilities = list(self._calculate_failure_probabilities())
        self.probabilities_of_error_free_operation = list(self._calculate_all_probabilities_of_error_free_operation())
        self.operating_time_to_failure = self._calculate_operating_time_to_failure()
        self.probability_of_error_free_operation = self._calculate_probability_of_error_free_operation(self.uptime)
        self.failure_intensity = self._calculate_failure_intensity()

    def _calculate_interval_borders(self):
        for i in range(0, self.max_time * self.num_of_intervals + 1, self.max_time):
            yield i / self.num_of_intervals

    def _calculate_failure_probabilities(self):
        for i in range(self.num_of_intervals):
            l = [time for time in self.work_times if self.interval_borders[i] < time <= self.interval_borders[i + 1]]
            yield len(l) / (len(self.work_times) * self.interval_length)

    def _calculate_all_probabilities_of_error_free_operation(self):
        for border in self.interval_borders:
            yield self._calculate_probability_of_error_free_operation(border)

    def _calculate_probability_of_error_free_operation(self, time):
        return 1 - (
            sum(self.failure_probabilities[0:int(time // self.interval_length)])
            * self.interval_length + self.safely_get(self.failure_probabilities, int(time // self.interval_length), 0) * (time % self.interval_length)
        )

    @staticmethod
    def safely_get(sequence, index, default=0):
        return sequence[index] if index < len(sequence) else default

    def _calculate_operating_time_to_failure(self):
        probabilities_less_or_equal_than_gamma = list(filter(lambda y: y <= self.gamma, self.probabilities_of_error_free_operation))
        idx = self.probabilities_of_error_free_operation.index(probabilities_less_or_equal_than_gamma[0])
        current_t_i = idx * self.interval_length
        previous_t_i = (idx - 1) * self.interval_length

        return (
            current_t_i - self.interval_length * (self._calculate_probability_of_error_free_operation(current_t_i) - self.gamma)
            / (self._calculate_probability_of_error_free_operation(current_t_i) - self._calculate_probability_of_error_free_operation(previous_t_i))
        )

    def _calculate_failure_intensity(self):
        return (
            self.failure_probabilities[int(self.lambda_uptime // self.interval_length)]
            / self._calculate_probability_of_error_free_operation(self.lambda_uptime)
        )


if __name__ == '__main__':
    work_times = [58,14,23,70,297,112,237,475,279,738,134,4,120,90,401,13,405,52,1007,19,77,12,32,259,46,518,52,0,172,512,13,1,119,128,310,131,235,284,79,16,69,18,305,461,12,93,85,348,48,146,121,39,126,415,419,28,39,516,65,2,36,192,34,21,346,622,617,59,330,580,80,6,960,234,52,438,170,75,92,340,403,177,113,55,87,51,165,58,1271,4,51,300,48,56,112,139,22,226,127,186]

    rel_ind = ReliablityIndicators(uptime=388, lambda_uptime=1012, gamma=0.89, work_times=work_times)
    rel_ind.run_calculations()

    print("Варіант 3, ІО-81, Гакман")
    print("=========")
    print(f"Наробіток до відмови (відсортований): {rel_ind.work_times}")
    print(f"Середній наробіток до відмови:        {rel_ind.average_time}")
    print(f"Максимальний наробіток до відмови:    {rel_ind.max_time}")
    print(f"Довжина інтрервалу:                   {rel_ind.interval_length}")
    print(f"Імовірності відмови:                  {rel_ind.failure_probabilities}")
    print(f"Імовірності безвідмовної роботи:      {rel_ind.probabilities_of_error_free_operation}")
    print(f"Y - відсотковий наробіток на відмову: {rel_ind.operating_time_to_failure}")
    print()
    print(f"Імовірність безвідмовної роботи ({rel_ind.uptime}): {rel_ind.probability_of_error_free_operation}")
    print(f"Інтенсивність відмов ({rel_ind.lambda_uptime}): {rel_ind.failure_intensity}")
