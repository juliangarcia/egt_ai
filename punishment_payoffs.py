# Language description

# 0 bit cooperation, C or D or L
# 1 bit, punish cooperators P or N
# 2 bit, punish defectors P or N
# 3 bit, punish loners P or N

def function_creator(i, j, r, c, sigma, beta_fine, gamma_cost, group_size, strategy_set):
        
        # PGG action
        
        is_i_loner=int(strategy_set[i][0] == "L")
        is_j_loner=int(strategy_set[j][0] == "L")
        
        does_i_cooperate = int(strategy_set[i][0] == "C")
        does_j_cooperate = int(strategy_set[j][0] == "C")
        
        does_i_defect = int(strategy_set[i][0] == "D")
        does_j_defect = int(strategy_set[j][0] == "D")
        
        #PUNISHMENT
        
        does_i_get_punished = None
        does_j_punish = None
        
        if does_i_cooperate and strategy_set[j][1]=='P':
            does_i_get_punished = True
            does_j_punish = True
        elif does_i_defect and strategy_set[j][2]=='P':
            does_i_get_punished = True
            does_j_punish = True
        elif is_i_loner and strategy_set[j][3]=='P':
            does_i_get_punished = True
            does_j_punish = True
        else:
            does_i_get_punished = False
            does_j_punish = False
        
        does_j_get_punished = None
        does_i_punish = None

        if does_j_cooperate and strategy_set[i][1]=='P':
            does_j_get_punished = True
            does_i_punish = True
        elif does_j_defect and strategy_set[i][2]=='P':
            does_j_get_punished = True
            does_i_punish = True
        elif is_j_loner and strategy_set[i][3]=='P':
            does_j_get_punished = True
            does_i_punish = True
        else:
            does_j_get_punished = False
            does_i_punish = False
            
        #SELF PUNISHMENT
        
        does_i_self_punish = False
        if does_i_cooperate and strategy_set[i][1]=='P':
            does_i_self_punish = True
        if does_i_defect and strategy_set[i][2]=='P':
            does_i_self_punish = True
        if is_i_loner and strategy_set[i][3]=='P':
            does_i_self_punish = True
        
        #does_j_self_punish = False doesnt matter

        
        def specific_function(k, group_size):
            # k i types
            # group_size - k types j
            
            
            # how many loners are there
            number_of_loners = k*is_i_loner + (group_size - k)*is_j_loner 
            effective_group_size = group_size - number_of_loners
            
            
            #benefit - cost cooperation - cost of punishment - fines
            
            #benefit
            number_of_cooperators = does_i_cooperate*k + (group_size -k)*does_j_cooperate
            benefit = 0.0
            if effective_group_size > 0:
                benefit = (number_of_cooperators*c*r)/effective_group_size
            
            cost_of_cooperation = 0.0
            if does_i_cooperate:
                cost_of_cooperation = c
                
            # below applies for loners too    
            
            cost_of_punishment = 0.0
            if does_i_punish:
                cost_of_punishment = gamma_cost*(group_size-k)
                
            fine = 0.0
            if does_i_get_punished:
                fine = beta_fine*(group_size-k)
                
                
            # self punishment
            if does_i_self_punish:
                fine =  fine  + (k-1)*beta_fine
                cost_of_punishment = cost_of_punishment + gamma_cost*(k-1)
                
            if effective_group_size < 2:
                return sigma
              
            if is_i_loner:
                return sigma - cost_of_punishment - fine
            
            # returns the expected payoff 
            return benefit - cost_of_cooperation - cost_of_punishment - fine
        return specific_function